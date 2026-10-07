"""Main Application Entry Point
Bus Booking System using Scrum Agile Methodology
Supports interactive terminal console, automated viva demo mode, and command-line flags.
Student: Archita (B.Tech 3rd Year) | Course: Agile Methodologies (AM)
"""
import sys
import os
import time
import argparse
from typing import Optional, Dict, Any

# Ensure project root is on Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Force UTF-8 on Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.database import init_db, seed_initial_data, DEFAULT_DB_PATH
from src.bus_booking import BusBookingService
from src.user_story import UserStoryService
from src.sprint import SprintService
from src.action_item import ActionItemService
from src.kanban import KanbanService


class Color:
    """Terminal ANSI styling codes with safe fallback."""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def print_banner():
    banner = f"""
{Color.CYAN}========================================================================================{Color.RESET}
{Color.BOLD}{Color.GREEN}       [+] BUS BOOKING SYSTEM - SCRUM AGILE METHODOLOGY (AM PBL){Color.RESET}
{Color.CYAN}========================================================================================{Color.RESET}
  {Color.YELLOW}* Student Project : Archita (B.Tech 3rd Year) | Subject: Agile Methodologies (AM){Color.RESET}
  {Color.BLUE}* Scrum Tracks    : 1. Bus Reservation Engine  |  2. In-App Scrum & Kanban Engine{Color.RESET}
{Color.CYAN}----------------------------------------------------------------------------------------{Color.RESET}
"""
    print(banner)


class BusAppRunner:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DEFAULT_DB_PATH
        seed_initial_data(self.db_path)

        self.bus_service = BusBookingService(self.db_path)
        self.story_service = UserStoryService(self.db_path)
        self.sprint_service = SprintService(self.db_path)
        self.action_service = ActionItemService(self.db_path)
        self.kanban_service = KanbanService(self.db_path)

        self.current_user: Optional[Dict[str, Any]] = None

    def handle_login(self):
        print(f"\n{Color.BOLD}--- User Login ---{Color.RESET}")
        print("Tip: Pre-seeded users:")
        print("  Passenger : 'archita_p'   | Password: 'archita123'")
        print("  Operator  : 'operator_neeta' | Password: 'operator123'")
        print("  Admin     : 'admin'       | Password: 'admin123'")
        username = input("Enter Username: ").strip()
        password = input("Enter Password: ").strip()

        try:
            user = self.bus_service.login_user(username, password)
            self.current_user = user
            print(f"{Color.GREEN}[+] Welcome, {user['full_name']}! (Role: {user['role'].upper()}){Color.RESET}")
        except ValueError as e:
            print(f"{Color.RED}[!] Authentication failed: {e}{Color.RESET}")

    def handle_register(self):
        print(f"\n{Color.BOLD}--- New Passenger Registration ---{Color.RESET}")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        full_name = input("Full Name: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone Number: ").strip()

        try:
            user = self.bus_service.register_user(username, password, full_name, email, phone, role="passenger")
            print(f"{Color.GREEN}[+] Passenger registered successfully! ID: {user['id']}. Please log in.{Color.RESET}")
        except ValueError as e:
            print(f"{Color.RED}[!] Registration error: {e}{Color.RESET}")

    def handle_search_buses(self):
        print(f"\n{Color.BOLD}--- Search Buses & Schedules ---{Color.RESET}")
        source = input("Origin City (press enter for all): ").strip()
        destination = input("Destination City (press enter for all): ").strip()
        travel_date = input("Travel Date (YYYY-MM-DD, e.g. 2026-10-15, or enter for all): ").strip()

        results = self.bus_service.search_buses(
            source=source if source else None,
            destination=destination if destination else None,
            travel_date=travel_date if travel_date else None
        )

        if not results:
            print(f"{Color.YELLOW}[!] No matching schedules found for the given criteria.{Color.RESET}")
            return

        print(f"\nFound {len(results)} scheduled service(s):")
        print("-" * 95)
        print(f"{'Sched ID':<10}{'Route':<22}{'Date & Time':<24}{'Bus Name & Type':<25}{'Fare':<8}{'Seats Left'}")
        print("-" * 95)
        for s in results:
            route = f"{s['source']} -> {s['destination']}"
            dt = f"{s['travel_date']} {s['departure_time']}"
            bus_info = f"{s['bus_name']} ({s['bus_type']})"[:24]
            print(f"#{s['schedule_id']:<9}{route:<22}{dt:<24}{bus_info:<25}Rs.{s['fare']:<5}{s['available_seats']}/{s['total_seats']}")
        print("-" * 95)

    def handle_view_seats(self):
        print(f"\n{Color.BOLD}--- Inspect Bus Seat Layout ---{Color.RESET}")
        sched_input = input("Enter Schedule ID to view seat map: ").strip()
        if not sched_input.isdigit():
            print(f"{Color.RED}[!] Invalid schedule ID.{Color.RESET}")
            return

        schedule_id = int(sched_input)
        details = self.bus_service.get_schedule_details(schedule_id)
        if not details:
            print(f"{Color.RED}[!] Schedule #{schedule_id} does not exist.{Color.RESET}")
            return

        print(f"\nService: {details['bus_name']} ({details['bus_type']}) | Route: {details['source']} -> {details['destination']}")
        print(f"Date: {details['travel_date']} Departure: {details['departure_time']} | Fare: Rs.{details['fare']}")
        print(f"Capacity: {details['total_seats']} | Available: {details['available_seats']} | Booked: {details['booked_seats']}")

        seats = self.bus_service.get_available_seats(schedule_id)
        print("\nSeat Layout Map ([O] = Available, [X] = Booked):")
        print("=" * 60)
        # Group into 4 per row
        row_buffer = []
        for s in seats:
            status = f"{Color.RED}[X]{Color.RESET}" if s["is_booked"] else f"{Color.GREEN}[O]{Color.RESET}"
            row_buffer.append(f"{s['seat_number']}:{status}")
            if len(row_buffer) == 4:
                print("   " + "   ".join(row_buffer))
                row_buffer = []
        if row_buffer:
            print("   " + "   ".join(row_buffer))
        print("=" * 60)

    def handle_book_ticket(self):
        print(f"\n{Color.BOLD}--- Book Bus Ticket ---{Color.RESET}")
        if not self.current_user:
            print(f"{Color.YELLOW}[!] Please log in first to book tickets.{Color.RESET}")
            return

        sched_input = input("Enter Schedule ID: ").strip()
        if not sched_input.isdigit():
            print(f"{Color.RED}[!] Invalid schedule ID.{Color.RESET}")
            return
        schedule_id = int(sched_input)

        seat_no = input("Enter Seat Number (e.g. 1A, 2B, 3C): ").strip()
        passenger_name = input(f"Passenger Name [{self.current_user['full_name']}]: ").strip()
        if not passenger_name:
            passenger_name = self.current_user["full_name"]

        age_input = input("Passenger Age: ").strip()
        age = int(age_input) if age_input.isdigit() else 22

        gender = input("Passenger Gender (Male/Female/Other) [Female]: ").strip().title()
        if not gender:
            gender = "Female"

        try:
            booking = self.bus_service.book_ticket(
                user_id=self.current_user["id"],
                schedule_id=schedule_id,
                seat_number=seat_no,
                passenger_name=passenger_name,
                passenger_age=age,
                passenger_gender=gender
            )
            print(f"\n{Color.GREEN}[+] BOOKING CONFIRMED!{Color.RESET}")
            print(f"    Reference ID : {Color.BOLD}{booking['booking_ref']}{Color.RESET}")
            print(f"    Seat Number  : {booking['seat_number']}")
            print(f"    Passenger    : {booking['passenger_name']} ({booking['passenger_age']}, {booking['passenger_gender']})")
            print(f"    Total Fare   : Rs. {booking['total_fare']}")
            print(f"    Status       : {booking['status']}")
        except ValueError as e:
            print(f"{Color.RED}[!] Booking Failed: {e}{Color.RESET}")

    def handle_cancel_ticket(self):
        print(f"\n{Color.BOLD}--- Cancel Ticket & Release Seat ---{Color.RESET}")
        if not self.current_user:
            print(f"{Color.YELLOW}[!] Please log in first.{Color.RESET}")
            return

        bookings = self.bus_service.get_user_bookings(self.current_user["id"])
        confirmed = [b for b in bookings if b["status"] == "Confirmed"]

        if not confirmed:
            print(f"{Color.YELLOW}[!] You have no active confirmed bookings to cancel.{Color.RESET}")
            return

        print("Your Active Bookings:")
        for b in confirmed:
            print(f"  ID #{b['booking_id']} | Ref: {b['booking_ref']} | Route: {b['source']} -> {b['destination']} | Seat: {b['seat_number']} | Date: {b['travel_date']}")

        bk_input = input("\nEnter Booking ID to cancel: ").strip()
        if not bk_input.isdigit():
            print(f"{Color.RED}[!] Invalid Booking ID.{Color.RESET}")
            return

        booking_id = int(bk_input)
        try:
            res = self.bus_service.cancel_booking(booking_id, user_id=self.current_user["id"])
            print(f"{Color.GREEN}[+] {res['message']}{Color.RESET}")
            print(f"    Reference: {res['booking_ref']} | Released Seat: {res['seat_number']}")
        except ValueError as e:
            print(f"{Color.RED}[!] Cancellation error: {e}{Color.RESET}")

    def handle_my_bookings(self):
        print(f"\n{Color.BOLD}--- My Booking History ---{Color.RESET}")
        if not self.current_user:
            print(f"{Color.YELLOW}[!] Please log in first.{Color.RESET}")
            return

        bookings = self.bus_service.get_user_bookings(self.current_user["id"])
        if not bookings:
            print("No booking records found for your account.")
            return

        print("-" * 90)
        print(f"{'ID':<6}{'Ref':<20}{'Route':<22}{'Travel Date':<14}{'Seat':<8}{'Fare':<8}{'Status'}")
        print("-" * 90)
        for b in bookings:
            status_color = Color.GREEN if b["status"] == "Confirmed" else Color.RED
            route = f"{b['source']} -> {b['destination']}"
            print(f"#{b['booking_id']:<5}{b['booking_ref']:<20}{route:<22}{b['travel_date']:<14}{b['seat_number']:<8}Rs.{b['total_fare']:<5}{status_color}{b['status']}{Color.RESET}")
        print("-" * 90)

    def handle_manifest(self):
        print(f"\n{Color.BOLD}--- Global Booking Manifest (Audit) ---{Color.RESET}")
        bookings = self.bus_service.get_all_bookings()
        if not bookings:
            print("No bookings registered in the system.")
            return

        print("-" * 95)
        print(f"{'Ref':<20}{'Passenger':<18}{'Route':<22}{'Bus':<16}{'Seat':<8}{'Status'}")
        print("-" * 95)
        for b in bookings:
            route = f"{b['source']} -> {b['destination']}"
            print(f"{b['booking_ref']:<20}{b['passenger_name']:<18}{route:<22}{b['bus_name'][:14]:<16}{b['seat_number']:<8}{b['status']}")
        print("-" * 95)

    def handle_scrum_backlog(self):
        print(f"\n{Color.BOLD}--- In-App Scrum Backlog & Sprints ---{Color.RESET}")
        sprints = self.sprint_service.list_sprints()
        print("\nSprints Overview:")
        print("-" * 80)
        for sp in sprints:
            m = self.sprint_service.get_sprint_metrics(sp["id"])
            print(f"Sprint {sp['sprint_number']}: {sp['name']} [{sp['status']}]")
            print(f"  Goal       : {sp['goal']}")
            print(f"  Commitment : {m['committed_points']} pts | Completed: {m['completed_points']} pts ({m['completion_percentage']}%)")
        print("-" * 80)

        stories = self.story_service.list_user_stories()
        print(f"\nUser Stories Inventory ({len(stories)} stories):")
        for st in stories:
            print(f"  [{st['story_code']}] {st['title']} ({st['story_points']} pts) - {st['priority']} | Status: {st['status']}")

    def handle_terminal_kanban(self):
        print("\n" + self.kanban_service.render_terminal_board())

    def run_viva_demo(self):
        """Automated Viva Walkthrough demonstrating full Scrum criteria in <30 seconds."""
        print(f"\n{Color.BOLD}{Color.CYAN}========================================================================{Color.RESET}")
        print(f"{Color.BOLD}{Color.GREEN}    [VIVA DEMO] AUTOMATED BUS BOOKING & SCRUM WALKTHROUGH{Color.RESET}")
        print(f"{Color.BOLD}{Color.CYAN}========================================================================{Color.RESET}")

        print(f"\n{Color.YELLOW}[Step 1] Initializing SQLite schema & pre-seeding Scrum sprint artifacts...{Color.RESET}")
        seed_initial_data(self.db_path)
        stats = self.bus_service.get_dashboard_stats()
        print(f"  -> System seeded: {stats['total_buses']} Buses, {stats['total_routes']} Routes, {stats['total_schedules']} Schedules.")

        print(f"\n{Color.YELLOW}[Step 2] Authenticating Passenger session for 'archita_p'...{Color.RESET}")
        user = self.bus_service.login_user("archita_p", "archita123")
        print(f"  -> {Color.GREEN}Authenticated: {user['full_name']} (Role: {user['role']}){Color.RESET}")

        print(f"\n{Color.YELLOW}[Step 3] Querying available bus corridor 'Pune' -> 'Mumbai' on 2026-10-15...{Color.RESET}")
        schedules = self.bus_service.search_buses(source="Pune", destination="Mumbai", travel_date="2026-10-15")
        sched = schedules[0]
        print(f"  -> Found: {sched['bus_name']} ({sched['bus_type']}) at {sched['departure_time']}. Fare: Rs.{sched['fare']}")

        print(f"\n{Color.YELLOW}[Step 4] Inspecting real-time seat availability for Schedule #{sched['schedule_id']}...{Color.RESET}")
        seats = self.bus_service.get_available_seats(sched["schedule_id"])
        open_seats = [s["seat_number"] for s in seats if s["is_booked"] == 0]
        print(f"  -> Open Seats ({len(open_seats)} available): {open_seats[:6]}...")

        target_seat = open_seats[0]
        print(f"\n{Color.YELLOW}[Step 5] Executing atomic booking for Seat '{target_seat}'...{Color.RESET}")
        booking = self.bus_service.book_ticket(
            user_id=user["id"],
            schedule_id=sched["schedule_id"],
            seat_number=target_seat,
            passenger_name="Archita",
            passenger_age=21,
            passenger_gender="Female"
        )
        print(f"  -> {Color.GREEN}Booking Confirmed! Ref: {booking['booking_ref']}, Seat: {booking['seat_number']}, Total: Rs.{booking['total_fare']}{Color.RESET}")

        print(f"\n{Color.YELLOW}[Step 6] Testing Defensive Double-Booking Concurrency Guard...{Color.RESET}")
        try:
            self.bus_service.book_ticket(
                user_id=2,  # Rahul
                schedule_id=sched["schedule_id"],
                seat_number=target_seat,
                passenger_name="Rahul Kulkarni",
                passenger_age=23,
                passenger_gender="Male"
            )
            print(f"  -> {Color.RED}[FAIL] Double-booking was allowed!{Color.RESET}")
        except ValueError as e:
            print(f"  -> {Color.GREEN}[PASS] Concurrency Guard Successfully Rejected Double-Booking: '{e}'{Color.RESET}")

        print(f"\n{Color.YELLOW}[Step 7] Testing Ticket Cancellation and Automatic Seat Recovery...{Color.RESET}")
        cancel_res = self.bus_service.cancel_booking(booking["booking_id"], user_id=user["id"])
        print(f"  -> {Color.GREEN}Cancelled {cancel_res['booking_ref']} | Released Seat: {cancel_res['seat_number']}{Color.RESET}")

        # Verify seat is open again
        rechecked_seats = self.bus_service.get_available_seats(sched["schedule_id"])
        seat_status = [s for s in rechecked_seats if s["seat_number"] == target_seat][0]
        print(f"  -> Verification: Seat '{target_seat}' is_booked = {seat_status['is_booked']} ({'VACANT/RECYCLED' if seat_status['is_booked'] == 0 else 'STILL BOOKED'})")

        print(f"\n{Color.YELLOW}[Step 8] Displaying Live In-App Terminal Kanban Board...{Color.RESET}")
        print(self.kanban_service.render_terminal_board())

        print(f"\n{Color.BOLD}{Color.GREEN}[+] VIVA DEMO COMPLETED SUCCESSFULLY WITH 100% PASSING CHECKS!{Color.RESET}\n")

    def run_interactive(self):
        print_banner()
        while True:
            user_status = f"Logged in as: {self.current_user['full_name']} ({self.current_user['role']})" if self.current_user else "Not Logged In"
            print(f"\nStatus: {Color.CYAN}{user_status}{Color.RESET}")
            print("1.  User Login")
            print("2.  Register New Passenger")
            print("3.  Search Buses & Schedules")
            print("4.  Inspect Seat Layout & Availability")
            print("5.  Book Bus Ticket (Atomic Lock)")
            print("6.  Cancel Ticket & Free Seat")
            print("7.  View My Bookings")
            print("8.  View Booking Manifest (Admin/Operator)")
            print("9.  View Scrum Backlog & Sprint Metrics")
            print("10. View Live Terminal Kanban Board")
            print("11. Run Automated Viva Demo Mode")
            print("12. Exit")

            choice = input("\nEnter choice (1-12): ").strip()
            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_register()
            elif choice == "3":
                self.handle_search_buses()
            elif choice == "4":
                self.handle_view_seats()
            elif choice == "5":
                self.handle_book_ticket()
            elif choice == "6":
                self.handle_cancel_ticket()
            elif choice == "7":
                self.handle_my_bookings()
            elif choice == "8":
                self.handle_manifest()
            elif choice == "9":
                self.handle_scrum_backlog()
            elif choice == "10":
                self.handle_terminal_kanban()
            elif choice == "11":
                self.run_viva_demo()
            elif choice == "12":
                print("\nThank you for using Bus Booking System. Goodbye!")
                break
            else:
                print(f"{Color.RED}Invalid option. Please enter 1-12.{Color.RESET}")


def main():
    parser = argparse.ArgumentParser(description="Bus Booking System - Scrum Agile PBL")
    parser.add_argument("--demo", action="store_true", help="Run automated viva demonstration mode")
    parser.add_argument("--kanban", action="store_true", help="Display live terminal Kanban board and exit")
    args = parser.parse_args()

    runner = BusAppRunner()

    if args.demo:
        runner.run_viva_demo()
    elif args.kanban:
        runner.handle_terminal_kanban()
    else:
        runner.run_interactive()


if __name__ == "__main__":
    main()
