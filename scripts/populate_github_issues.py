"""Script to populate GitHub Issues, Labels, and Milestones
Uses the GitHub REST API to synchronize the project's User Stories and Action Items
with color-coded priority labels (High = Red, Medium = Orange/Yellow, Low = Green).
Target Repository: yashkarwa2005/bus-booking-system
Student: Archita | Course: Agile Methodologies & IT (AM)
"""
import urllib.request
import urllib.error
import urllib.parse
import json
import time
import os
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def get_token():
    env_token = os.environ.get("GITHUB_TOKEN", "")
    if env_token:
        return env_token
    try:
        proc = subprocess.Popen(
            "git credential fill",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        out, _ = proc.communicate(input="protocol=https\nhost=github.com\n")
        for line in out.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1].strip()
    except Exception as e:
        print(f"[-] Could not read credential manager: {e}")
    return ""


OWNER = "yashkarwa2005"
REPO = "bus-booking-system"
TOKEN = get_token()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "Agile-PBL-Setup",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github+json"
}


def api_request(endpoint, method="GET", data=None):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/{endpoint}"
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8") if data else None,
        headers=HEADERS,
        method=method
    )
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        return {"error": e.code, "message": err_msg}


def create_or_update_label(name, color, description):
    res = api_request("labels", method="POST", data={
        "name": name,
        "color": color,
        "description": description
    })
    if "error" in res and res["error"] == 422:
        safe_name = urllib.parse.quote(name)
        api_request(f"labels/{safe_name}", method="PATCH", data={
            "color": color,
            "description": description
        })
    print(f"[*] Label '{name}' configured with color #{color}")


def create_milestones():
    milestones = [
        ("Sprint 1 - Identity, Authentication & Architecture", "Deliver user registration, authentication and database architecture.", 1),
        ("Sprint 2 - Bus Fleet, Route Network & Schedules", "Deliver bus fleet catalog, route mapping, and timetable scheduling.", 2),
        ("Sprint 3 - Corridor Search & Atomic Booking Lock", "Implement origin-destination search and atomic reservation lock.", 3),
        ("Sprint 4 - Cancellation & Seat Recovery", "Support full ticket lifecycle with automatic seat vacancy recycling.", 4),
        ("Sprint 5 - Scrum Engine, Tests & Viva Release", "Integrate in-app Scrum/Kanban board, test coverage, and final viva release.", 5),
    ]
    created = {}
    for title, desc, num in milestones:
        res = api_request("milestones", method="POST", data={
            "title": title,
            "description": desc,
            "state": "closed" if num <= 4 else "open"
        })
        if "number" in res:
            created[num] = res["number"]
            print(f"[+] Milestone created: {title} (ID #{res['number']})")
        else:
            # Check existing milestones
            existing = api_request("milestones?state=all")
            if isinstance(existing, list):
                for m in existing:
                    if m["title"] == title:
                        created[num] = m["number"]
                        print(f"[*] Found existing milestone: {title} (ID #{m['number']})")
    return created


def main():
    if not TOKEN:
        print("[!] No GitHub token found. Please set GITHUB_TOKEN or check git credentials.")
        return

    print("=== Step 1: Setting up Agile Labels with Color Coding ===")
    labels = [
        # MoSCoW & Priority Labels
        ("priority: high", "d73a4a", "High Priority - Must Have"),
        ("priority: medium", "fbca04", "Medium Priority - Should Have"),
        ("priority: low", "0e8a16", "Low Priority - Could Have"),
        # Type Labels
        ("type: user-story", "1d76db", "Scrum User Story card"),
        ("type: task", "5319e7", "Technical Sprint Task"),
        ("type: testing", "006b75", "Automated Testing & QA"),
        ("type: documentation", "0075ca", "Architecture & Scrum Documentation"),
        # Status Labels
        ("status: backlog", "cfd3d7", "In Product Backlog"),
        ("status: todo", "1d76db", "Committed to Sprint To Do"),
        ("status: in-progress", "d93f0b", "Currently in development"),
        ("status: review-testing", "a2eeef", "Under testing and review"),
        ("status: done", "0e8a16", "Completed and verified against DoD"),
    ]
    for name, color, desc in labels:
        create_or_update_label(name, color, desc)

    print("\n=== Step 2: Creating Sprint Milestones ===")
    milestone_map = create_milestones()

    print("\n=== Step 3: Populating User Stories as GitHub Issues ===")
    user_stories = [
        {
            "code": "US-01",
            "title": "Passenger & Operator Registration",
            "body": """### User Story
**As a** new passenger or bus operator,  
**I want** to register an account using my username, email, and password,  
**So that** I can securely access the bus booking platform.

### Story Points: 3 | Priority: High (Must Have)
### Target Sprint: Sprint 1 | Assignee: Archita

### Acceptance Criteria
- [x] Validates unique username and email.
- [x] Hashes passwords securely with salted SHA-256.
- [x] Prevents duplicate accounts.
""",
            "priority": "priority: high",
            "sprint": 1,
            "status": "status: done"
        },
        {
            "code": "US-02",
            "title": "Credential Authentication & Role Session",
            "body": """### User Story
**As a** registered user,  
**I want** to log in using my credentials,  
**So that** the system loads my authorized role interface.

### Story Points: 3 | Priority: High (Must Have)
### Target Sprint: Sprint 1 | Assignee: Dev Team

### Acceptance Criteria
- [x] Verifies salted SHA-256 hash against stored record.
- [x] Rejects invalid credentials cleanly.
- [x] Assigns session role (passenger, operator, admin).
""",
            "priority": "priority: high",
            "sprint": 1,
            "status": "status: done"
        },
        {
            "code": "US-03",
            "title": "Bus Fleet & Seating Specifications Management",
            "body": """### User Story
**As a** bus operator,  
**I want** to add and manage buses with seating configurations,  
**So that** operators can register fleet capacity.

### Story Points: 5 | Priority: High (Must Have)
### Target Sprint: Sprint 2 | Assignee: Archita

### Acceptance Criteria
- [x] Registers bus registration number, bus name, and type.
- [x] Configures seat capacity between 10 and 60 seats.
- [x] Rejects duplicate bus numbers.
""",
            "priority": "priority: high",
            "sprint": 2,
            "status": "status: done"
        },
        {
            "code": "US-04",
            "title": "Route Network & Distance Definition",
            "body": """### User Story
**As a** bus operator,  
**I want** to define intercity travel corridors with distance and duration,  
**So that** the system maps valid travel options.

### Story Points: 5 | Priority: High (Must Have)
### Target Sprint: Sprint 2 | Assignee: Dev Team

### Acceptance Criteria
- [x] Validates origin and destination cities.
- [x] Prevents identical origin and destination.
- [x] Records distance (km) and travel duration (hours).
""",
            "priority": "priority: high",
            "sprint": 2,
            "status": "status: done"
        },
        {
            "code": "US-05",
            "title": "Bus Timetable & Fare Scheduling",
            "body": """### User Story
**As a** bus operator,  
**I want** to publish bus timetables with departure time, arrival time, and fare,  
**So that** passengers can view and book scheduled departures.

### Story Points: 3 | Priority: High (Must Have)
### Target Sprint: Sprint 2 | Assignee: Dev Team

### Acceptance Criteria
- [x] Links bus, route, travel date, departure time, and fare.
- [x] Auto-generates seat inventory records upon schedule creation.
""",
            "priority": "priority: high",
            "sprint": 2,
            "status": "status: done"
        },
        {
            "code": "US-06",
            "title": "Search Buses by Origin, Destination & Date",
            "body": """### User Story
**As a** passenger,  
**I want** to search available buses by source, destination, and travel date,  
**So that** I can compare departures and fares.

### Story Points: 5 | Priority: High (Must Have)
### Target Sprint: Sprint 3 | Assignee: Dev Team

### Acceptance Criteria
- [x] Case-insensitive search by origin and destination.
- [x] Displays bus name, type, departure, fare, and available seats.
""",
            "priority": "priority: high",
            "sprint": 3,
            "status": "status: done"
        },
        {
            "code": "US-07",
            "title": "Real-Time Seat Layout & Vacancy Inspection",
            "body": """### User Story
**As a** passenger,  
**I want** to view a visual seat layout showing booked vs open seats,  
**So that** I can select my preferred seat.

### Story Points: 3 | Priority: High (Must Have)
### Target Sprint: Sprint 3 | Assignee: Dev Team

### Acceptance Criteria
- [x] Returns seat matrix distinguishing booked from open seats.
- [x] Classifies window vs aisle seats.
""",
            "priority": "priority: high",
            "sprint": 3,
            "status": "status: done"
        },
        {
            "code": "US-08",
            "title": "Atomic Seat Reservation & Double-Booking Lock",
            "body": """### User Story
**As a** passenger,  
**I want** to reserve my chosen seat atomically,  
**So that** no other passenger can double-book the same seat.

### Story Points: 8 | Priority: High (Must Have)
### Target Sprint: Sprint 3 | Assignee: Archita

### Acceptance Criteria
- [x] Atomic SQLite transaction locking seat immediately.
- [x] Concurrency check aborting conflicting bookings.
- [x] Unique booking reference generated (BK-YYYYMMDD-XXXX).
""",
            "priority": "priority: high",
            "sprint": 3,
            "status": "status: done"
        },
        {
            "code": "US-09",
            "title": "Passenger Itinerary History & E-Ticket Details",
            "body": """### User Story
**As a** passenger,  
**I want** to view my active and past booking history,  
**So that** I have proof of travel and itinerary reference.

### Story Points: 3 | Priority: Medium (Should Have)
### Target Sprint: Sprint 4 | Assignee: Dev Team

### Acceptance Criteria
- [x] Returns all bookings for authenticated passenger.
- [x] Shows bus, route, date, seat, and status.
""",
            "priority": "priority: medium",
            "sprint": 4,
            "status": "status: done"
        },
        {
            "code": "US-10",
            "title": "Ticket Cancellation & Immediate Seat Recovery",
            "body": """### User Story
**As a** passenger,  
**I want** to cancel an existing ticket reservation,  
**So that** my seat is immediately recycled for other passengers to book.

### Story Points: 5 | Priority: High (Must Have)
### Target Sprint: Sprint 4 | Assignee: Archita

### Acceptance Criteria
- [x] Sets booking status to Cancelled.
- [x] Atomically resets seat is_booked = 0.
- [x] Prevents duplicate cancellation.
""",
            "priority": "priority: high",
            "sprint": 4,
            "status": "status: done"
        },
        {
            "code": "US-11",
            "title": "Operator Passenger Manifest & Fleet Audit",
            "body": """### User Story
**As an** operator or administrator,  
**I want** to view all passenger bookings across buses,  
**So that** I can audit vehicle occupancy and revenue.

### Story Points: 3 | Priority: Low (Could Have)
### Target Sprint: Sprint 5 | Assignee: Dev Team

### Acceptance Criteria
- [x] Centralized view across all departures and passengers.
""",
            "priority": "priority: low",
            "sprint": 5,
            "status": "status: done"
        },
        {
            "code": "US-12",
            "title": "In-App Scrum Backlog, Sprint & Kanban Engine",
            "body": """### User Story
**As a** Scrum team member,  
**I want** to track user stories and Kanban board within the software,  
**So that** our team practices transparent Agile software engineering.

### Story Points: 8 | Priority: High (Must Have)
### Target Sprint: Sprint 5 | Assignee: Archita

### Acceptance Criteria
- [x] Persistent SQLite user stories and sprints tables.
- [x] Terminal ASCII Kanban board with 5 columns.
- [x] Web interactive Kanban board at /kanban.
""",
            "priority": "priority: high",
            "sprint": 5,
            "status": "status: done"
        }
    ]

    for st in user_stories:
        data = {
            "title": st["title"],
            "body": st["body"],
            "labels": [st["priority"], "type: user-story", st["status"]],
        }
        if st["sprint"] in milestone_map:
            data["milestone"] = milestone_map[st["sprint"]]

        res = api_request("issues", method="POST", data=data)
        if "number" in res:
            print(f"[+] Created Issue #{res['number']}: {st['title']}")
        else:
            print(f"[-] Issue error: {res}")
        time.sleep(0.3)

    print("\n[SUCCESS] All labels, milestones, and issues created on GitHub with color coding!")


if __name__ == "__main__":
    main()
