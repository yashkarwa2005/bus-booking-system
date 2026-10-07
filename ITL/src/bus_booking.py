"""Bus Booking Service Module
Handles business logic for:
  - User registration & authentication with salted SHA-256
  - Bus, route, and schedule management
  - Schedule search by origin, destination, and travel date
  - Real-time seat layout queries & vacancy calculation
  - Atomic ticket booking with defensive double-booking concurrency lock
  - Self-service ticket cancellation with immediate seat vacancy recycling
  - Passenger itinerary history and administrative audit manifest
"""
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
import sqlite3

from src.database import get_connection, hash_password


class BusBookingService:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    # =========================================================================
    # 1. Identity & Access Management (US-01, US-02)
    # =========================================================================

    def register_user(
        self,
        username: str,
        password: str,
        full_name: str,
        email: str,
        phone: str = "",
        role: str = "passenger"
    ) -> Dict[str, Any]:
        """Registers a new user (passenger, operator, admin) with salted SHA-256 hashing."""
        username = username.strip()
        full_name = full_name.strip()
        email = email.strip().lower()

        if not username or not password or not full_name or not email:
            raise ValueError("All mandatory fields (username, password, full_name, email) are required.")

        if role not in ("passenger", "operator", "admin"):
            raise ValueError("Role must be 'passenger', 'operator', or 'admin'.")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        # Check existing username or email
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?;", (username, email))
        if cursor.fetchone():
            conn.close()
            raise ValueError("Username or Email is already registered.")

        pwd_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, password_hash, full_name, email, phone, role)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (username, pwd_hash, full_name, email, phone, role))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return {
            "id": user_id,
            "username": username,
            "full_name": full_name,
            "email": email,
            "role": role
        }

    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticates user credentials and returns session user dictionary."""
        username = username.strip()
        if not username or not password:
            raise ValueError("Username and password must not be empty.")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, password_hash, full_name, email, phone, role
            FROM users WHERE username = ?;
        """, (username,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            raise ValueError("Invalid username or password.")

        if row["password_hash"] != hash_password(password):
            raise ValueError("Invalid username or password.")

        return {
            "id": row["id"],
            "username": row["username"],
            "full_name": row["full_name"],
            "email": row["email"],
            "phone": row["phone"],
            "role": row["role"]
        }

    # =========================================================================
    # 2. Fleet & Route Management (US-03, US-04, US-05)
    # =========================================================================

    def add_bus(
        self,
        bus_number: str,
        bus_name: str,
        bus_type: str,
        total_seats: int = 24,
        operator_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Registers a new bus with seating capacity."""
        bus_number = bus_number.strip().upper()
        bus_name = bus_name.strip()

        if not bus_number or not bus_name:
            raise ValueError("Bus number and bus name are required.")

        valid_types = ('AC Sleeper', 'AC Semi-Sleeper', 'Non-AC Sleeper', 'Volvo Multi-Axle', 'Deluxe')
        if bus_type not in valid_types:
            raise ValueError(f"Invalid bus type. Must be one of {valid_types}.")

        if total_seats < 10 or total_seats > 60:
            raise ValueError("Total seats must be between 10 and 60.")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO buses (bus_number, bus_name, bus_type, total_seats, operator_id)
                VALUES (?, ?, ?, ?, ?);
            """, (bus_number, bus_name, bus_type, total_seats, operator_id))
            bus_id = cursor.lastrowid
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError(f"Bus with registration '{bus_number}' already exists.")
        conn.close()

        return {
            "id": bus_id,
            "bus_number": bus_number,
            "bus_name": bus_name,
            "bus_type": bus_type,
            "total_seats": total_seats
        }

    def list_buses(self) -> List[Dict[str, Any]]:
        """Returns all registered buses."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.id, b.bus_number, b.bus_name, b.bus_type, b.total_seats, b.operator_id,
                   u.full_name AS operator_name
            FROM buses b
            LEFT JOIN users u ON b.operator_id = u.id
            ORDER BY b.id ASC;
        """)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def add_route(
        self,
        source: str,
        destination: str,
        distance_km: float,
        duration_hours: float
    ) -> Dict[str, Any]:
        """Registers a new travel corridor."""
        source = source.strip().title()
        destination = destination.strip().title()

        if not source or not destination:
            raise ValueError("Source and destination are required.")
        if source.lower() == destination.lower():
            raise ValueError("Source and destination cannot be identical.")
        if distance_km <= 0 or duration_hours <= 0:
            raise ValueError("Distance and duration must be positive values.")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO routes (source, destination, distance_km, duration_hours)
            VALUES (?, ?, ?, ?);
        """, (source, destination, distance_km, duration_hours))
        route_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return {
            "id": route_id,
            "source": source,
            "destination": destination,
            "distance_km": distance_km,
            "duration_hours": duration_hours
        }

    def list_routes(self) -> List[Dict[str, Any]]:
        """Returns all registered routes."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM routes ORDER BY source ASC, destination ASC;")
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def add_schedule(
        self,
        bus_id: int,
        route_id: int,
        travel_date: str,
        departure_time: str,
        arrival_time: str,
        fare: float
    ) -> Dict[str, Any]:
        """Publishes a new bus timetable and auto-initializes the seat layout matrix."""
        if fare <= 0:
            raise ValueError("Fare must be greater than zero.")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        # Validate bus existence and seat count
        cursor.execute("SELECT id, total_seats, bus_type FROM buses WHERE id = ?;", (bus_id,))
        bus = cursor.fetchone()
        if not bus:
            conn.close()
            raise ValueError(f"Bus with ID {bus_id} not found.")

        # Validate route existence
        cursor.execute("SELECT id FROM routes WHERE id = ?;", (route_id,))
        if not cursor.fetchone():
            conn.close()
            raise ValueError(f"Route with ID {route_id} not found.")

        cursor.execute("""
            INSERT INTO schedules (bus_id, route_id, travel_date, departure_time, arrival_time, fare, status)
            VALUES (?, ?, ?, ?, ?, ?, 'Scheduled');
        """, (bus_id, route_id, travel_date, departure_time, arrival_time, fare))
        schedule_id = cursor.lastrowid

        # Generate seats automatically based on total_seats
        total = bus["total_seats"]
        seats_to_insert = []
        rows_count = (total // 4) + (1 if total % 4 != 0 else 0)
        seat_num = 1
        for r in range(1, rows_count + 1):
            for col in ['A', 'B', 'C', 'D']:
                if seat_num > total:
                    break
                stype = "Window" if col in ('A', 'D') else "Aisle"
                if "Sleeper" in bus["bus_type"]:
                    stype = "Sleeper-Lower" if r <= (rows_count // 2) else "Sleeper-Upper"
                seats_to_insert.append((schedule_id, f"{r}{col}", stype, 0))
                seat_num += 1

        cursor.executemany("""
            INSERT INTO seats (schedule_id, seat_number, seat_type, is_booked)
            VALUES (?, ?, ?, ?);
        """, seats_to_insert)

        conn.commit()
        conn.close()

        return {
            "id": schedule_id,
            "bus_id": bus_id,
            "route_id": route_id,
            "travel_date": travel_date,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "fare": fare,
            "seats_created": len(seats_to_insert)
        }

    # =========================================================================
    # 3. Schedule Search & Seat Inspection (US-06, US-07)
    # =========================================================================

    def search_buses(
        self,
        source: Optional[str] = None,
        destination: Optional[str] = None,
        travel_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Searches available bus schedules with optional source, destination, and travel date filters."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        query = """
            SELECT s.id AS schedule_id, s.travel_date, s.departure_time, s.arrival_time, s.fare, s.status,
                   b.id AS bus_id, b.bus_number, b.bus_name, b.bus_type, b.total_seats,
                   r.id AS route_id, r.source, r.destination, r.distance_km, r.duration_hours,
                   (SELECT COUNT(*) FROM seats WHERE schedule_id = s.id AND is_booked = 0) AS available_seats
            FROM schedules s
            JOIN buses b ON s.bus_id = b.id
            JOIN routes r ON s.route_id = r.id
            WHERE s.status = 'Scheduled'
        """
        params: List[Any] = []

        if source and source.strip():
            query += " AND LOWER(r.source) LIKE LOWER(?)"
            params.append(f"%{source.strip()}%")

        if destination and destination.strip():
            query += " AND LOWER(r.destination) LIKE LOWER(?)"
            params.append(f"%{destination.strip()}%")

        if travel_date and travel_date.strip():
            query += " AND s.travel_date = ?"
            params.append(travel_date.strip())

        query += " ORDER BY s.travel_date ASC, s.departure_time ASC;"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_schedule_details(self, schedule_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves complete schedule details including route, bus, and seat statistics."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id AS schedule_id, s.travel_date, s.departure_time, s.arrival_time, s.fare, s.status,
                   b.bus_number, b.bus_name, b.bus_type, b.total_seats,
                   r.source, r.destination, r.distance_km, r.duration_hours,
                   (SELECT COUNT(*) FROM seats WHERE schedule_id = s.id AND is_booked = 0) AS available_seats,
                   (SELECT COUNT(*) FROM seats WHERE schedule_id = s.id AND is_booked = 1) AS booked_seats
            FROM schedules s
            JOIN buses b ON s.bus_id = b.id
            JOIN routes r ON s.route_id = r.id
            WHERE s.id = ?;
        """, (schedule_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_available_seats(self, schedule_id: int) -> List[Dict[str, Any]]:
        """Returns the full seat map layout (both booked and unbooked) for interactive seat selection."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, seat_number, seat_type, is_booked
            FROM seats
            WHERE schedule_id = ?
            ORDER BY LENGTH(seat_number), seat_number ASC;
        """, (schedule_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    # =========================================================================
    # 4. Atomic Booking Engine & Concurrency Guard (US-08)
    # =========================================================================

    def book_ticket(
        self,
        user_id: int,
        schedule_id: int,
        seat_number: str,
        passenger_name: str,
        passenger_age: int,
        passenger_gender: str
    ) -> Dict[str, Any]:
        """Atomically reserves a seat and creates a booking record.
        Enforces a concurrency lock: if the seat is already booked, transaction aborts.
        """
        seat_number = seat_number.strip().upper()
        passenger_name = passenger_name.strip()
        passenger_gender = passenger_gender.strip().title()

        if not seat_number or not passenger_name:
            raise ValueError("Seat number and passenger name are required.")
        if passenger_age <= 0 or passenger_age > 120:
            raise ValueError("Passenger age must be between 1 and 120.")
        if passenger_gender not in ('Male', 'Female', 'Other'):
            raise ValueError("Gender must be 'Male', 'Female', or 'Other'.")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("BEGIN IMMEDIATE;")

            # 1. Inspect schedule & fare
            cursor.execute("SELECT fare, travel_date, departure_time, status FROM schedules WHERE id = ?;", (schedule_id,))
            sched = cursor.fetchone()
            if not sched:
                conn.rollback()
                raise ValueError(f"Schedule ID {schedule_id} does not exist.")
            if sched["status"] != "Scheduled":
                conn.rollback()
                raise ValueError(f"Cannot book tickets for a schedule in status '{sched['status']}'.")

            fare = sched["fare"]

            # 2. Concurrency Lock: Inspect seat availability
            cursor.execute("""
                SELECT id, is_booked FROM seats
                WHERE schedule_id = ? AND UPPER(seat_number) = ?;
            """, (schedule_id, seat_number))
            seat = cursor.fetchone()

            if not seat:
                conn.rollback()
                raise ValueError(f"Seat '{seat_number}' does not exist on this bus schedule.")

            if seat["is_booked"] == 1:
                conn.rollback()
                raise ValueError(f"Concurrency Conflict: Seat '{seat_number}' is already booked.")

            seat_id = seat["id"]

            # 3. Lock seat atomically
            cursor.execute("UPDATE seats SET is_booked = 1 WHERE id = ?;", (seat_id,))

            # 4. Generate unique booking reference
            timestamp_str = datetime.now().strftime("%Y%m%d")
            unique_suffix = uuid.uuid4().hex[:4].upper()
            booking_ref = f"BK-{timestamp_str}-{unique_suffix}"

            # 5. Insert booking record
            cursor.execute("""
                INSERT INTO bookings (
                    booking_ref, user_id, schedule_id, seat_id, seat_number,
                    passenger_name, passenger_age, passenger_gender, total_fare, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Confirmed');
            """, (
                booking_ref, user_id, schedule_id, seat_id, seat_number,
                passenger_name, passenger_age, passenger_gender, fare
            ))
            booking_id = cursor.lastrowid

            # 6. Log audit event
            cursor.execute("""
                INSERT INTO audit_logs (action_type, user_id, user_name, details)
                VALUES ('TICKET_BOOKED', ?, ?, ?);
            """, (user_id, passenger_name, f"Booked seat {seat_number} on schedule {schedule_id} (Ref: {booking_ref})"))

            conn.commit()

            return {
                "booking_id": booking_id,
                "booking_ref": booking_ref,
                "schedule_id": schedule_id,
                "seat_number": seat_number,
                "passenger_name": passenger_name,
                "passenger_age": passenger_age,
                "passenger_gender": passenger_gender,
                "total_fare": fare,
                "status": "Confirmed"
            }

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # =========================================================================
    # 5. Ticket Cancellation & Seat Recovery (US-10)
    # =========================================================================

    def cancel_booking(self, booking_id: int, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Atomically cancels a confirmed ticket booking and immediately recycles the seat vacancy."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("BEGIN IMMEDIATE;")

            query = "SELECT * FROM bookings WHERE id = ?;"
            params: List[Any] = [booking_id]
            if user_id is not None:
                query = "SELECT * FROM bookings WHERE id = ? AND user_id = ?;"
                params.append(user_id)

            cursor.execute(query, params)
            booking = cursor.fetchone()

            if not booking:
                conn.rollback()
                raise ValueError(f"Booking #{booking_id} not found or permission denied.")

            if booking["status"] == "Cancelled":
                conn.rollback()
                raise ValueError(f"Booking #{booking_id} is already cancelled.")

            # 1. Update booking status to Cancelled
            cursor.execute("UPDATE bookings SET status = 'Cancelled' WHERE id = ?;", (booking_id,))

            # 2. Release seat atomically
            seat_id = booking["seat_id"]
            cursor.execute("UPDATE seats SET is_booked = 0 WHERE id = ?;", (seat_id,))

            # 3. Log audit event
            cursor.execute("""
                INSERT INTO audit_logs (action_type, user_id, user_name, details)
                VALUES ('TICKET_CANCELLED', ?, ?, ?);
            """, (
                booking["user_id"],
                booking["passenger_name"],
                f"Cancelled booking {booking['booking_ref']} and recycled seat {booking['seat_number']}."
            ))

            conn.commit()

            return {
                "booking_id": booking_id,
                "booking_ref": booking["booking_ref"],
                "seat_number": booking["seat_number"],
                "status": "Cancelled",
                "message": "Booking successfully cancelled and seat vacancy recycled."
            }

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # =========================================================================
    # 6. Passenger History & Manifest Queries (US-09, US-11)
    # =========================================================================

    def get_user_bookings(self, user_id: int) -> List[Dict[str, Any]]:
        """Returns all bookings belonging to a specific passenger in reverse chronological order."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bk.id AS booking_id, bk.booking_ref, bk.seat_number, bk.passenger_name,
                   bk.passenger_age, bk.passenger_gender, bk.total_fare, bk.status, bk.booking_date,
                   s.travel_date, s.departure_time, s.arrival_time,
                   b.bus_number, b.bus_name, b.bus_type,
                   r.source, r.destination
            FROM bookings bk
            JOIN schedules s ON bk.schedule_id = s.id
            JOIN buses b ON s.bus_id = b.id
            JOIN routes r ON s.route_id = r.id
            WHERE bk.user_id = ?
            ORDER BY bk.id DESC;
        """, (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_all_bookings(self) -> List[Dict[str, Any]]:
        """Returns the global booking manifest across all routes and buses for admin oversight."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bk.id AS booking_id, bk.booking_ref, bk.seat_number, bk.passenger_name,
                   bk.passenger_age, bk.passenger_gender, bk.total_fare, bk.status, bk.booking_date,
                   u.username AS booked_by,
                   s.travel_date, s.departure_time,
                   b.bus_number, b.bus_name,
                   r.source, r.destination
            FROM bookings bk
            JOIN users u ON bk.user_id = u.id
            JOIN schedules s ON bk.schedule_id = s.id
            JOIN buses b ON s.bus_id = b.id
            JOIN routes r ON s.route_id = r.id
            ORDER BY bk.id DESC;
        """)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Provides aggregate operational statistics for dashboard and viva presentation."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) AS total_passengers FROM users WHERE role = 'passenger';")
        passengers = cursor.fetchone()["total_passengers"]

        cursor.execute("SELECT COUNT(*) AS total_buses FROM buses;")
        buses = cursor.fetchone()["total_buses"]

        cursor.execute("SELECT COUNT(*) AS total_routes FROM routes;")
        routes = cursor.fetchone()["total_routes"]

        cursor.execute("SELECT COUNT(*) AS total_schedules FROM schedules WHERE status = 'Scheduled';")
        schedules = cursor.fetchone()["total_schedules"]

        cursor.execute("SELECT COUNT(*) AS total_bookings, COALESCE(SUM(total_fare), 0) AS total_revenue FROM bookings WHERE status = 'Confirmed';")
        booking_stat = cursor.fetchone()

        conn.close()
        return {
            "total_passengers": passengers,
            "total_buses": buses,
            "total_routes": routes,
            "total_schedules": schedules,
            "total_bookings": booking_stat["total_bookings"],
            "total_revenue": booking_stat["total_revenue"]
        }
