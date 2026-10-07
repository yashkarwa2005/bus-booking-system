"""BusFlow - Online Bus Booking System (AM PBL Submission)
Standalone Python Web Application with Embedded REST API & Responsive Dashboard.
Zero mandatory external dependencies - uses standard library http.server + sqlite3.
Student: Archita (B.Tech 3rd Year) | Course: Agile Methodologies & IT (AM)
"""
import os
import sys
import json
import sqlite3
import urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import webbrowser
import threading
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.database import get_connection, seed_initial_data, DEFAULT_DB_PATH
from src.bus_booking import BusBookingService
from src.user_story import UserStoryService
from src.sprint import SprintService
from src.action_item import ActionItemService
from src.kanban import KanbanService

DEFAULT_PORT = 5000


def log_audit(action_type: str, user_id: int, user_name: str, details: str):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            INSERT INTO audit_logs (action_type, user_id, user_name, details)
            VALUES (?, ?, ?, ?);
        """, (action_type, user_id, user_name, details))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[-] Audit log error: {e}")


class BusFlowRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

    def send_json(self, data, status_code=200):
        body = json.dumps(data, default=str).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, message, status_code=400):
        self.send_json({"error": message}, status_code=status_code)

    def parse_body(self):
        content_len = int(self.headers.get("Content-Length", 0))
        if content_len == 0:
            return {}
        raw = self.rfile.read(content_len).decode("utf-8")
        try:
            return json.loads(raw)
        except Exception:
            return urllib.parse.parse_qs(raw)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # 1. Frontend Homepage
        if path == "/" or path == "/index.html":
            template_path = os.path.join(BASE_DIR, "templates", "index.html")
            if os.path.exists(template_path):
                with open(template_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                self.send_error(404, "Template index.html not found")
                return

        # 2. Kanban Board HTML
        if path == "/kanban" or path == "/kanban_board.html":
            kb_path = os.path.join(BASE_DIR, "kanban_board.html")
            if os.path.exists(kb_path):
                with open(kb_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                self.send_error(404, "kanban_board.html not found")
                return

        svc = BusBookingService()

        # 3. API: Stats
        if path == "/api/stats":
            stats = svc.get_dashboard_stats()
            self.send_json(stats)
            return

        # 4. API: Buses
        if path == "/api/buses":
            self.send_json(svc.list_buses())
            return

        # 5. API: Routes
        if path == "/api/routes":
            self.send_json(svc.list_routes())
            return

        # 6. API: Schedules Search
        if path == "/api/schedules":
            src = query.get("source", [None])[0]
            dst = query.get("destination", [None])[0]
            dt = query.get("date", [None])[0]
            schedules = svc.search_buses(source=src, destination=dst, travel_date=dt)
            self.send_json(schedules)
            return

        # 7. API: Seats for a Schedule
        if path == "/api/seats":
            sched_id_str = query.get("schedule_id", [None])[0]
            if not sched_id_str or not sched_id_str.isdigit():
                self.send_error_json("Parameter 'schedule_id' is required.")
                return
            seats = svc.get_available_seats(int(sched_id_str))
            self.send_json(seats)
            return

        # 8. API: Bookings (User or Global)
        if path == "/api/bookings":
            user_id_str = query.get("user_id", [None])[0]
            if user_id_str and user_id_str.isdigit():
                self.send_json(svc.get_user_bookings(int(user_id_str)))
            else:
                self.send_json(svc.get_all_bookings())
            return

        # 9. API: Kanban Board Data
        if path == "/api/kanban":
            kb = KanbanService()
            self.send_json(kb.get_board_data())
            return

        # 10. API: Sprints
        if path == "/api/sprints":
            sp_svc = SprintService()
            sprints = sp_svc.list_sprints()
            metrics = [sp_svc.get_sprint_metrics(s["id"]) for s in sprints]
            self.send_json(metrics)
            return

        # 11. API: Audit Logs
        if path == "/api/audit-logs":
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 50;")
            logs = [dict(r) for r in c.fetchall()]
            conn.close()
            self.send_json(logs)
            return

        self.send_error(404, "Endpoint Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self.parse_body()
        svc = BusBookingService()

        # 1. API: User Login
        if path == "/api/login":
            username = body.get("username", "")
            password = body.get("password", "")
            try:
                user = svc.login_user(username, password)
                self.send_json({"success": True, "user": user})
            except ValueError as e:
                self.send_error_json(str(e), 401)
            return

        # 2. API: User Registration
        if path == "/api/register":
            try:
                user = svc.register_user(
                    username=body.get("username", ""),
                    password=body.get("password", ""),
                    full_name=body.get("full_name", ""),
                    email=body.get("email", ""),
                    phone=body.get("phone", ""),
                    role=body.get("role", "passenger")
                )
                self.send_json({"success": True, "user": user}, 201)
            except ValueError as e:
                self.send_error_json(str(e), 400)
            return

        # 3. API: Book Ticket (Atomic Transaction)
        if path == "/api/book":
            try:
                booking = svc.book_ticket(
                    user_id=int(body.get("user_id", 1)),
                    schedule_id=int(body.get("schedule_id")),
                    seat_number=str(body.get("seat_number", "")),
                    passenger_name=str(body.get("passenger_name", "")),
                    passenger_age=int(body.get("passenger_age", 25)),
                    passenger_gender=str(body.get("passenger_gender", "Female"))
                )
                self.send_json({"success": True, "booking": booking}, 201)
            except Exception as e:
                self.send_error_json(str(e), 400)
            return

        # 4. API: Cancel Booking
        if path == "/api/cancel":
            try:
                booking_id = int(body.get("booking_id"))
                user_id = body.get("user_id")
                uid = int(user_id) if user_id else None
                res = svc.cancel_booking(booking_id, uid)
                self.send_json({"success": True, "result": res})
            except Exception as e:
                self.send_error_json(str(e), 400)
            return

        # 5. API: Move Kanban Card
        if path == "/api/kanban/move":
            code = body.get("code", "")
            target_col = body.get("target_column", "")
            try:
                if code.startswith("US-"):
                    story_svc = UserStoryService()
                    updated = story_svc.update_status(code, target_col)
                    self.send_json({"success": True, "card": updated})
                elif code.startswith("AI-"):
                    action_svc = ActionItemService()
                    # map column to action status
                    col_map = {"To Do": "To Do", "In Progress": "In Progress", "Review/Testing": "Review", "Done": "Done"}
                    updated = action_svc.update_status(code, col_map.get(target_col, "In Progress"))
                    self.send_json({"success": True, "card": updated})
                else:
                    self.send_error_json("Unrecognized card identifier", 400)
            except Exception as e:
                self.send_error_json(str(e), 400)
            return

        self.send_error(404, "Endpoint Not Found")


def run_server(port=DEFAULT_PORT, auto_open=True):
    seed_initial_data()
    server_address = ("127.0.0.1", port)
    httpd = ThreadingHTTPServer(server_address, BusFlowRequestHandler)
    url = f"http://127.0.0.1:{port}"
    print(f"\n[+] BusFlow Server live at: {url}")
    print(f"[+] Kanban Board available at: {url}/kanban")
    print("Press Ctrl+C to stop.\n")

    if auto_open:
        threading.Thread(target=lambda: (time.sleep(1), webbrowser.open(url))).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()


if __name__ == "__main__":
    port = DEFAULT_PORT
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_server(port=port, auto_open=False)
