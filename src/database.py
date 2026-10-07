"""Database Module for Bus Booking System
Manages SQLite connection, schema definition, foreign key enforcement, and seed data.
Supports dual-track architecture:
  1. Bus Booking & Reservation Engine
  2. In-App Scrum & Agile Project Management Engine
"""
import os
import sqlite3
import hashlib
from typing import Optional

DEFAULT_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database")
DEFAULT_DB_PATH = os.path.join(DEFAULT_DB_DIR, "bus_booking.db")


def hash_password(password: str, salt: str = "bus_scrum_salt_2026") -> str:
    """Hashes a password with salt using SHA-256."""
    return hashlib.sha256(f"{salt}_{password}".encode("utf-8")).hexdigest()


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Returns a SQLite connection with foreign keys enabled and row_factory set to sqlite3.Row."""
    if db_path is None:
        db_path = DEFAULT_DB_PATH
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    elif db_path != ":memory:":
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: Optional[str] = None) -> None:
    """Creates database schema if tables do not exist."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        role TEXT NOT NULL CHECK(role IN ('passenger', 'operator', 'admin')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Buses Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_number TEXT UNIQUE NOT NULL,
        bus_name TEXT NOT NULL,
        bus_type TEXT NOT NULL CHECK(bus_type IN ('AC Sleeper', 'AC Semi-Sleeper', 'Non-AC Sleeper', 'Volvo Multi-Axle', 'Deluxe')),
        total_seats INTEGER NOT NULL DEFAULT 30,
        operator_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 3. Routes Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        destination TEXT NOT NULL,
        distance_km REAL NOT NULL,
        duration_hours REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 4. Schedules Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_id INTEGER NOT NULL REFERENCES buses(id) ON DELETE CASCADE,
        route_id INTEGER NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
        travel_date TEXT NOT NULL,
        departure_time TEXT NOT NULL,
        arrival_time TEXT NOT NULL,
        fare REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'Scheduled' CHECK(status IN ('Scheduled', 'Departed', 'Completed', 'Cancelled')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 5. Seats Table (Specific to a schedule)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS seats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        schedule_id INTEGER NOT NULL REFERENCES schedules(id) ON DELETE CASCADE,
        seat_number TEXT NOT NULL,
        seat_type TEXT NOT NULL CHECK(seat_type IN ('Window', 'Aisle', 'Sleeper-Lower', 'Sleeper-Upper')),
        is_booked INTEGER DEFAULT 0 CHECK(is_booked IN (0, 1)),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(schedule_id, seat_number)
    );
    """)

    # 6. Bookings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_ref TEXT UNIQUE NOT NULL,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        schedule_id INTEGER NOT NULL REFERENCES schedules(id) ON DELETE CASCADE,
        seat_id INTEGER NOT NULL REFERENCES seats(id),
        seat_number TEXT NOT NULL,
        passenger_name TEXT NOT NULL,
        passenger_age INTEGER NOT NULL,
        passenger_gender TEXT NOT NULL,
        total_fare REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'Confirmed' CHECK(status IN ('Confirmed', 'Cancelled', 'Completed')),
        booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 7. Sprints Table (Scrum Management)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sprints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sprint_number INTEGER UNIQUE NOT NULL,
        name TEXT NOT NULL,
        goal TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Planning' CHECK(status IN ('Planning', 'Active', 'Completed')),
        velocity INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 8. User Stories Table (Product Backlog & Sprint Backlog)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        story_code TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        role TEXT NOT NULL,
        want TEXT NOT NULL,
        benefit TEXT NOT NULL,
        priority TEXT NOT NULL CHECK(priority IN ('Must Have', 'Should Have', 'Could Have', 'Won''t Have')),
        story_points INTEGER NOT NULL,
        sprint_id INTEGER REFERENCES sprints(id) ON DELETE SET NULL,
        status TEXT NOT NULL DEFAULT 'Backlog' CHECK(status IN ('Backlog', 'To Do', 'In Progress', 'Review/Testing', 'Done')),
        assignee TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 9. Action Items Table (Sprint Action Items & Standups)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS action_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_code TEXT UNIQUE NOT NULL,
        description TEXT NOT NULL,
        sprint_id INTEGER REFERENCES sprints(id) ON DELETE SET NULL,
        owner TEXT NOT NULL,
        priority TEXT NOT NULL CHECK(priority IN ('High', 'Medium', 'Low')),
        due_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'To Do' CHECK(status IN ('To Do', 'In Progress', 'Review', 'Done', 'Blocked')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 10. Audit Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_type TEXT NOT NULL,
        user_id INTEGER,
        user_name TEXT,
        details TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


def seed_initial_data(db_path: Optional[str] = None) -> None:
    """Populates realistic initial data for demonstration and testing if the DB is empty."""
    init_db(db_path)
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS count FROM users;")
    if cursor.fetchone()["count"] > 0:
        conn.close()
        return  # Data already seeded

    # --- Seed Users ---
    users_data = [
        ("archita_p", hash_password("archita123"), "Archita", "archita@example.com", "9820011223", "passenger"),
        ("rahul_k", hash_password("rahul123"), "Rahul Kulkarni", "rahul.k@example.com", "9820044556", "passenger"),
        ("operator_neeta", hash_password("operator123"), "Suresh Joshi (Neeta Operator)", "operator@neetabus.com", "9890012345", "operator"),
        ("admin", hash_password("admin123"), "System Administrator", "admin@busbooking.local", "9800000000", "admin"),
    ]
    cursor.executemany("""
    INSERT INTO users (username, password_hash, full_name, email, phone, role)
    VALUES (?, ?, ?, ?, ?, ?);
    """, users_data)

    # --- Seed Buses ---
    buses_data = [
        ("MH-12-RN-4501", "Shivneri Volvo Multi-Axle", "Volvo Multi-Axle", 24, 3),
        ("MH-02-AB-9821", "Neeta Royal Sleeper", "AC Sleeper", 20, 3),
        ("KA-01-MJ-3310", "VRL Premier Semi-Sleeper", "AC Semi-Sleeper", 28, 3),
        ("MH-14-CZ-7744", "Purple Travels Deluxe", "Deluxe", 32, 3),
    ]
    cursor.executemany("""
    INSERT INTO buses (bus_number, bus_name, bus_type, total_seats, operator_id)
    VALUES (?, ?, ?, ?, ?);
    """, buses_data)

    # --- Seed Routes ---
    routes_data = [
        ("Pune", "Mumbai", 150.0, 3.5),
        ("Mumbai", "Goa", 580.0, 11.5),
        ("Pune", "Bangalore", 840.0, 14.0),
        ("Mumbai", "Pune", 150.0, 3.5),
        ("Pune", "Goa", 460.0, 9.0),
    ]
    cursor.executemany("""
    INSERT INTO routes (source, destination, distance_km, duration_hours)
    VALUES (?, ?, ?, ?);
    """, routes_data)

    # --- Seed Schedules ---
    schedules_data = [
        (1, 1, "2026-10-15", "06:00 AM", "09:30 AM", 650.0, "Scheduled"),
        (1, 1, "2026-10-15", "02:00 PM", "05:30 PM", 650.0, "Scheduled"),
        (2, 2, "2026-10-15", "08:00 PM", "07:30 AM", 1450.0, "Scheduled"),
        (3, 3, "2026-10-16", "05:30 PM", "07:30 AM", 1850.0, "Scheduled"),
        (4, 4, "2026-10-15", "07:00 AM", "10:30 AM", 550.0, "Scheduled"),
        (1, 5, "2026-10-16", "09:00 PM", "06:00 AM", 1200.0, "Scheduled"),
    ]
    cursor.executemany("""
    INSERT INTO schedules (bus_id, route_id, travel_date, departure_time, arrival_time, fare, status)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """, schedules_data)

    # --- Seed Seats for Schedules ---
    # For schedule 1 (Shivneri Volvo, 24 seats: 1A-6D)
    seat_records = []
    for sched_id in range(1, 7):
        # Generate 20 to 24 seats per schedule
        total = 24 if sched_id in (1, 2, 6) else 20
        for i in range(1, (total // 4) + 1):
            for col in ['A', 'B', 'C', 'D']:
                stype = "Window" if col in ['A', 'D'] else "Aisle"
                if sched_id == 3:  # Sleeper
                    stype = "Sleeper-Lower" if i <= 3 else "Sleeper-Upper"
                seat_records.append((sched_id, f"{i}{col}", stype, 0))

    cursor.executemany("""
    INSERT INTO seats (schedule_id, seat_number, seat_type, is_booked)
    VALUES (?, ?, ?, ?);
    """, seat_records)

    # --- Seed Sample Booking ---
    # Reserve seat 1A and 1B on schedule 1 for Archita
    cursor.execute("""
    UPDATE seats SET is_booked = 1 WHERE schedule_id = 1 AND seat_number = '1A';
    """)
    cursor.execute("""
    SELECT id FROM seats WHERE schedule_id = 1 AND seat_number = '1A';
    """)
    seat_1a_id = cursor.fetchone()["id"]

    cursor.execute("""
    INSERT INTO bookings (booking_ref, user_id, schedule_id, seat_id, seat_number, passenger_name, passenger_age, passenger_gender, total_fare, status)
    VALUES ('BK-20261015-8492', 1, 1, ?, '1A', 'Archita', 21, 'Female', 650.0, 'Confirmed');
    """, (seat_1a_id,))

    # --- Seed Sprints (Scrum Methodology) ---
    sprints_data = [
        (1, "Sprint 1: Identity & Foundation", "Deliver user registration, authentication, role-based access, and core SQLite schema.", "2026-09-01", "2026-09-07", "Completed", 6),
        (2, "Sprint 2: Bus, Route & Fleet Operations", "Implement bus catalog, route network mapping, and schedule generation.", "2026-09-08", "2026-09-14", "Completed", 13),
        (3, "Sprint 3: Discovery & Concurrency Lock", "Deliver origin-destination bus search, seat map visualization, and atomic reservation lock.", "2026-09-15", "2026-09-21", "Completed", 16),
        (4, "Sprint 4: Ticket Lifecycle & Seat Recovery", "Enable ticket cancellation, seat recycling, and passenger booking history tracking.", "2026-09-22", "2026-09-28", "Completed", 10),
        (5, "Sprint 5: In-App Scrum Tooling & Release", "Integrate in-app Kanban board, automated unit test suite, and final viva release.", "2026-09-29", "2026-10-07", "Completed", 16),
    ]
    cursor.executemany("""
    INSERT INTO sprints (sprint_number, name, goal, start_date, end_date, status, velocity)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """, sprints_data)

    # --- Seed User Stories (Product Backlog) ---
    stories_data = [
        ("US-01", "Passenger & Operator Registration", "Passenger", "register an account with encrypted credentials", "I can access the bus booking platform securely", "Must Have", 3, 1, "Done", "Archita", "Password salted SHA-256 and unique user validation"),
        ("US-02", "Credential Authentication & Role Session", "All Roles", "log in with valid credentials", "the system loads my authorized role interface", "Must Have", 3, 1, "Done", "Dev Team", "Role-based authorization for passenger, operator, admin"),
        ("US-03", "Bus Fleet & Fleet Specifications Management", "Operator", "add and manage buses with seat configurations", "operators can register fleet capacity", "Must Have", 5, 2, "Done", "Archita", "Bus number, type, seating configuration"),
        ("US-04", "Route Network & Distance Definition", "Operator", "define bus routes with origin, destination, and distance", "the system knows viable travel corridors", "Must Have", 5, 2, "Done", "Dev Team", "Source, destination, duration and km mapping"),
        ("US-05", "Bus Timetable & Fare Scheduling", "Operator", "publish bus schedules with departure, arrival, and fare", "passengers can inspect planned departures", "Must Have", 3, 2, "Done", "Dev Team", "Schedule linking bus, route, date and pricing"),
        ("US-06", "Search Bus by Source, Destination & Date", "Passenger", "search available buses between cities on a travel date", "I can identify suitable travel options", "Must Have", 5, 3, "Done", "Dev Team", "Case-insensitive query by corridor and departure date"),
        ("US-07", "Dynamic Seat Map & Availability Inspection", "Passenger", "view real-time seat layout showing booked vs open seats", "I can choose my preferred window or aisle seat", "Must Have", 3, 3, "Done", "Dev Team", "Visual matrix of available and booked seat cards"),
        ("US-08", "Atomic Seat Reservation & Double-Booking Lock", "Passenger", "atomically book a seat with instant locking", "no other passenger can double-book the same seat", "Must Have", 8, 3, "Done", "Archita", "ACID SQLite transaction preventing race conditions"),
        ("US-09", "Passenger Booking History & Ticket Detail", "Passenger", "view all past and active ticket reservations", "I can track my travel itinerary and reference IDs", "Should Have", 3, 4, "Done", "Dev Team", "Chronological history with departure time and status"),
        ("US-10", "Ticket Cancellation & Atomic Seat Recycling", "Passenger", "cancel a confirmed booking and immediately release the seat", "the seat becomes available for other passengers to book", "Must Have", 5, 4, "Done", "Archita", "Sets booking to Cancelled and unlocks seat is_booked=0"),
        ("US-11", "Operator Passenger Manifest & Fleet Audit", "Operator", "view all passenger bookings across buses and routes", "fleet managers can audit occupancy and revenue", "Could Have", 3, 5, "Done", "Dev Team", "Centralized administrative manifest oversight"),
        ("US-12", "In-App Scrum Backlog, Sprint & Kanban Engine", "Scrum Team", "track agile user stories and Kanban board within the application", "our team practices transparent Agile software engineering", "Must Have", 8, 5, "Done", "Archita", "Integrated SQLite-backed 5-column Kanban engine"),
    ]
    cursor.executemany("""
    INSERT INTO user_stories (story_code, title, role, want, benefit, priority, story_points, sprint_id, status, assignee, description)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, stories_data)

    # --- Seed Action Items ---
    actions_data = [
        ("AI-01", "Initialize GitHub repository and clean .gitignore rules", 1, "Archita", "High", "2026-09-02", "Done"),
        ("AI-02", "Design relational SQLite schema with foreign key cascades", 1, "Dev Team", "High", "2026-09-04", "Done"),
        ("AI-03", "Implement SHA-256 password salting and authentication service", 1, "Archita", "High", "2026-09-06", "Done"),
        ("AI-04", "Draft INVEST User Stories and Gherkin Acceptance Criteria", 1, "Archita", "Medium", "2026-09-07", "Done"),
        ("AI-05", "Implement Bus Fleet and Seating Layout models", 2, "Dev Team", "High", "2026-09-10", "Done"),
        ("AI-06", "Construct Route directory and schedule publishing service", 2, "Archita", "High", "2026-09-12", "Done"),
        ("AI-07", "Populate realistic bus routes (Pune-Mumbai, Mumbai-Goa, Bangalore)", 2, "Dev Team", "Low", "2026-09-14", "Done"),
        ("AI-08", "Build origin-destination bus schedule search query", 3, "Dev Team", "High", "2026-09-17", "Done"),
        ("AI-09", "Implement dynamic seat layout matrix and vacancy counter", 3, "Dev Team", "High", "2026-09-19", "Done"),
        ("AI-10", "Engineer atomic seat booking transaction with double-booking guard", 3, "Archita", "High", "2026-09-21", "Done"),
        ("AI-11", "Implement booking cancellation and automatic seat vacancy recovery", 4, "Archita", "High", "2026-09-24", "Done"),
        ("AI-12", "Construct passenger booking history and e-ticket summary generator", 4, "Dev Team", "Medium", "2026-09-26", "Done"),
        ("AI-13", "Develop operator passenger manifest and occupancy inspection tool", 5, "Dev Team", "Medium", "2026-09-30", "Done"),
        ("AI-14", "Implement SQLite-backed in-app Scrum Backlog & Sprint Service", 5, "Archita", "High", "2026-10-02", "Done"),
        ("AI-15", "Construct interactive terminal ASCII Kanban board renderer", 5, "Archita", "High", "2026-10-03", "Done"),
        ("AI-16", "Write 16 automated unit and integration tests with 100% pass rate", 5, "Archita", "High", "2026-10-04", "Done"),
        ("AI-17", "Prepare architecture diagrams, ERD, and academic documentation", 5, "Dev Team", "Medium", "2026-10-05", "Done"),
        ("AI-18", "Push verified commits, tags, and synchronize GitHub repository", 5, "Archita", "High", "2026-10-07", "Done"),
    ]
    cursor.executemany("""
    INSERT INTO action_items (item_code, description, sprint_id, owner, priority, due_date, status)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """, actions_data)

    # --- Seed Initial Audit Logs ---
    audit_data = [
        ("SYSTEM_INIT", 4, "System Administrator", "Database schema initialized with SQLite foreign key enforcement."),
        ("FLEET_SETUP", 3, "Suresh Joshi (Neeta Operator)", "Configured 4 buses and 5 intercity travel routes."),
        ("INITIAL_RESERVATION", 1, "Archita", "Confirmed booking BK-20261015-8492 on Pune-Mumbai Shivneri Express (Seat 1A)."),
    ]
    cursor.executemany("""
    INSERT INTO audit_logs (action_type, user_id, user_name, details)
    VALUES (?, ?, ?, ?);
    """, audit_data)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    seed_initial_data()
    print("[+] Database initialized and seeded successfully.")
