"""Comprehensive Automated Test Suite for Bus Booking System
Course: Agile Methodologies & IT (AM) PBL | Student: Archita
Covers:
  - User Registration & Salted Hashing (US-01)
  - Credential Authentication & Role Sessions (US-02)
  - Fleet & Route Management (US-03, US-04, US-05)
  - Schedule Search & Seat Map Queries (US-06, US-07)
  - Atomic Reservation & Double-Booking Lock (US-08)
  - Itinerary History & Cancellation Seat Recovery (US-09, US-10)
  - Administrative Oversight & Audit (US-11)
  - In-App Scrum Backlog, Sprints & Kanban Engine (US-12)
"""
import os
import unittest
import tempfile
from src.database import init_db, seed_initial_data, get_connection
from src.bus_booking import BusBookingService
from src.user_story import UserStoryService
from src.sprint import SprintService
from src.action_item import ActionItemService
from src.kanban import KanbanService


class TestBusBookingSystem(unittest.TestCase):
    def setUp(self):
        """Creates an isolated temporary SQLite database for each test case."""
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_file.close()
        self.db_path = self.temp_file.name
        seed_initial_data(self.db_path)

        self.bus_service = BusBookingService(self.db_path)
        self.story_service = UserStoryService(self.db_path)
        self.sprint_service = SprintService(self.db_path)
        self.action_service = ActionItemService(self.db_path)
        self.kanban_service = KanbanService(self.db_path)

    def tearDown(self):
        """Cleans up temporary database file after test completion."""
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    # =========================================================================
    # TC-01 & TC-02: User Registration Tests (US-01)
    # =========================================================================

    def test_tc01_user_registration_success(self):
        """TC-01: Verify successful passenger registration with valid credentials."""
        user = self.bus_service.register_user(
            username="priya_sharma",
            password="SecurePass@123",
            full_name="Priya Sharma",
            email="priya.sharma@example.com",
            phone="9811223344",
            role="passenger"
        )
        self.assertIsNotNone(user["id"])
        self.assertEqual(user["username"], "priya_sharma")
        self.assertEqual(user["role"], "passenger")

    def test_tc02_duplicate_user_registration_rejection(self):
        """TC-02: Verify duplicate username or email is rejected."""
        with self.assertRaises(ValueError):
            self.bus_service.register_user(
                username="archita_p",  # Already in seed data
                password="AnotherPassword",
                full_name="Duplicate Archita",
                email="different.email@example.com",
                role="passenger"
            )

    # =========================================================================
    # TC-03 & TC-04: User Authentication Tests (US-02)
    # =========================================================================

    def test_tc03_user_login_success(self):
        """TC-03: Verify successful authentication with valid credentials."""
        user = self.bus_service.login_user("archita_p", "archita123")
        self.assertEqual(user["username"], "archita_p")
        self.assertEqual(user["role"], "passenger")

    def test_tc04_user_login_invalid_credentials_rejected(self):
        """TC-04: Verify rejection of invalid username or incorrect password."""
        with self.assertRaises(ValueError):
            self.bus_service.login_user("archita_p", "wrong_password")
        with self.assertRaises(ValueError):
            self.bus_service.login_user("non_existent_user", "pass123")

    # =========================================================================
    # TC-05 & TC-06: Fleet & Route Management (US-03, US-04)
    # =========================================================================

    def test_tc05_add_bus_success(self):
        """TC-05: Verify operator can register a new bus with seat capacity."""
        bus = self.bus_service.add_bus(
            bus_number="DL-01-AB-1234",
            bus_name="Rajdhani Superfast Volvo",
            bus_type="Volvo Multi-Axle",
            total_seats=28
        )
        self.assertIsNotNone(bus["id"])
        self.assertEqual(bus["bus_number"], "DL-01-AB-1234")
        self.assertEqual(bus["total_seats"], 28)

    def test_tc06_add_route_and_validation(self):
        """TC-06: Verify route creation and rejection of identical source and destination."""
        route = self.bus_service.add_route(
            source="Mumbai",
            destination="Ahmedabad",
            distance_km=520.0,
            duration_hours=8.5
        )
        self.assertIsNotNone(route["id"])
        self.assertEqual(route["source"], "Mumbai")
        self.assertEqual(route["destination"], "Ahmedabad")

        # Identity validation check
        with self.assertRaises(ValueError):
            self.bus_service.add_route("Pune", "Pune", 0, 0)

    # =========================================================================
    # TC-07 & TC-08: Schedule Publication & Search (US-05, US-06)
    # =========================================================================

    def test_tc07_add_schedule_and_auto_seat_generation(self):
        """TC-07: Verify schedule generation auto-populates seat inventory."""
        sched = self.bus_service.add_schedule(
            bus_id=1,
            route_id=1,
            travel_date="2026-11-01",
            departure_time="08:00 AM",
            arrival_time="11:30 AM",
            fare=700.0
        )
        self.assertIsNotNone(sched["id"])
        self.assertEqual(sched["seats_created"], 24)

        # Inspect seats
        seats = self.bus_service.get_available_seats(sched["id"])
        self.assertEqual(len(seats), 24)
        self.assertTrue(all(s["is_booked"] == 0 for s in seats))

    def test_tc08_search_buses_by_corridor(self):
        """TC-08: Verify origin-destination search returns available schedules."""
        results = self.bus_service.search_buses(source="Pune", destination="Mumbai")
        self.assertGreater(len(results), 0)
        for r in results:
            self.assertEqual(r["source"], "Pune")
            self.assertEqual(r["destination"], "Mumbai")

    # =========================================================================
    # TC-09, TC-10 & TC-11: Atomic Booking & Concurrency Lock (US-07, US-08)
    # =========================================================================

    def test_tc09_inspect_seat_map_availability(self):
        """TC-09: Verify seat map inspection correctly distinguishes booked and open seats."""
        seats = self.bus_service.get_available_seats(schedule_id=1)
        # In seed data, seat 1A is booked
        seat_1a = next(s for s in seats if s["seat_number"] == "1A")
        self.assertEqual(seat_1a["is_booked"], 1)

        seat_1b = next(s for s in seats if s["seat_number"] == "1B")
        self.assertEqual(seat_1b["is_booked"], 0)

    def test_tc10_atomic_booking_success(self):
        """TC-10: Verify atomic ticket reservation locks seat and returns booking ref."""
        booking = self.bus_service.book_ticket(
            user_id=1,
            schedule_id=1,
            seat_number="1B",
            passenger_name="Archita",
            passenger_age=21,
            passenger_gender="Female"
        )
        self.assertIsNotNone(booking["booking_id"])
        self.assertTrue(booking["booking_ref"].startswith("BK-"))
        self.assertEqual(booking["seat_number"], "1B")
        self.assertEqual(booking["status"], "Confirmed")

        # Verify seat is marked booked in DB
        seats = self.bus_service.get_available_seats(1)
        seat_1b = next(s for s in seats if s["seat_number"] == "1B")
        self.assertEqual(seat_1b["is_booked"], 1)

    def test_tc11_double_booking_concurrency_rejection(self):
        """TC-11: Verify defensive concurrency guard blocks duplicate booking of same seat."""
        # Seat 1A is already booked in seed data
        with self.assertRaises(ValueError) as ctx:
            self.bus_service.book_ticket(
                user_id=2,
                schedule_id=1,
                seat_number="1A",
                passenger_name="Rahul Kulkarni",
                passenger_age=24,
                passenger_gender="Male"
            )
        self.assertIn("already booked", str(ctx.exception).lower())

    # =========================================================================
    # TC-12 & TC-13: Ticket Cancellation & Seat Recovery (US-09, US-10)
    # =========================================================================

    def test_tc12_cancellation_and_automatic_seat_recycling(self):
        """TC-12: Verify ticket cancellation marks status Cancelled and recycles seat to is_booked=0."""
        # Book seat 1C first
        booking = self.bus_service.book_ticket(
            user_id=1,
            schedule_id=1,
            seat_number="1C",
            passenger_name="Archita",
            passenger_age=21,
            passenger_gender="Female"
        )
        booking_id = booking["booking_id"]

        # Cancel the booking
        cancel_res = self.bus_service.cancel_booking(booking_id, user_id=1)
        self.assertEqual(cancel_res["status"], "Cancelled")

        # Verify seat 1C is immediately recycled
        seats = self.bus_service.get_available_seats(1)
        seat_1c = next(s for s in seats if s["seat_number"] == "1C")
        self.assertEqual(seat_1c["is_booked"], 0)

    def test_tc13_passenger_booking_history(self):
        """TC-13: Verify passenger can retrieve their chronological booking history."""
        bookings = self.bus_service.get_user_bookings(user_id=1)
        self.assertGreater(len(bookings), 0)
        self.assertEqual(bookings[0]["passenger_name"], "Archita")

    # =========================================================================
    # TC-14: Operator Manifest & Auditing (US-11)
    # =========================================================================

    def test_tc14_global_manifest_and_stats(self):
        """TC-14: Verify administrative oversight returns manifest and summary stats."""
        manifest = self.bus_service.get_all_bookings()
        self.assertGreater(len(manifest), 0)

        stats = self.bus_service.get_dashboard_stats()
        self.assertGreater(stats["total_buses"], 0)
        self.assertGreater(stats["total_schedules"], 0)

    # =========================================================================
    # TC-15 & TC-16: Scrum Engine, Sprints & Kanban (US-12)
    # =========================================================================

    def test_tc15_scrum_user_story_lifecycle(self):
        """TC-15: Verify creation, validation, and Kanban status transition of user stories."""
        story = self.story_service.create_user_story(
            story_code="US-TEST-01",
            title="Real-time GPS Tracking",
            role="Passenger",
            want="track bus live location on map",
            benefit="I know exact arrival time",
            priority="Could Have",
            story_points=5,
            sprint_id=5,
            status="To Do",
            assignee="Archita"
        )
        self.assertEqual(story["story_code"], "US-TEST-01")

        # Transition status
        updated = self.story_service.update_status("US-TEST-01", "In Progress")
        self.assertEqual(updated["status"], "In Progress")

    def test_tc16_sprint_metrics_and_kanban_rendering(self):
        """TC-16: Verify sprint metrics and ASCII Kanban board generation."""
        metrics = self.sprint_service.get_sprint_metrics(sprint_id=1)
        self.assertGreater(metrics["committed_points"], 0)

        board_str = self.kanban_service.render_terminal_board()
        self.assertIn("BUS BOOKING SYSTEM", board_str)
        self.assertIn("BACKLOG", board_str)
        self.assertIn("DONE", board_str)


if __name__ == "__main__":
    unittest.main()
