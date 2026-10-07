# Sprint Plan (5-Week Scrum Iteration Schedule)
## Bus Booking System using Scrum Agile Methodology

---

## 1. Scrum Cadence & Team Roles

The project was executed across **5 weekly Sprint iterations** (7 calendar days per sprint):

### Scrum Roles:
- **Product Owner:** Archita — Defines the product vision, maintains and prioritizes the Product Backlog, and accepts completed increments based on Acceptance Criteria.
- **Scrum Master:** Facilitator — Runs Daily Scrums, Sprint Planning, Reviews, and Retrospectives; clears technical impediments.
- **Development Team (Led by Archita):** Full-stack developers responsible for relational schema design, concurrency locking algorithms, CLI/Web interfaces, and automated test cases.

---

## 2. Weekly Sprint Breakdown

---

### 🚀 SPRINT 1 (Week 1)
**Theme:** User Authentication, Role Management & Core Architecture
- **Sprint Goal:** Establish the SQLite database architecture and deliver a secure, testable user registration and session authentication system.
- **Sprint Duration:** Week 1
- **Committed Points:** 6 Points
- **Completed Points:** 6 Points
- **Status:** 🟢 Completed

#### User Stories in Sprint 1:
| Story ID | Story Title | Priority | Story Points | Assignee |
|---|---|---|---|---|
| `US-01` | Passenger & Operator Registration | 🔴 Must Have | 3 | Archita |
| `US-02` | Credential Authentication & Role Session | 🔴 Must Have | 3 | Dev Team |

#### Task Breakdown:
1. Initialize repository, `.gitignore`, and folder structure. (Owner: Archita, Est: 2h)
2. Design and implement `src/database.py` with `users` schema and foreign key enforcement. (Owner: Dev Team, Est: 3h)
3. Implement salted SHA-256 password hashing. (Owner: Archita, Est: 2h)
4. Build `register_user` and `login_user` in `src/bus_booking.py`. (Owner: Dev Team, Est: 3h)
5. Create automated test cases `TC-01`, `TC-02`, `TC-03`, `TC-04`. (Owner: Archita, Est: 2h)

- **Expected Increment:** Working authentication engine where users register with unique usernames/emails, passwords are encrypted, and logins return valid user sessions.
- **Actual Increment Delivered:** 100% delivered with zero defects.

---

### 🚀 SPRINT 2 (Week 2)
**Theme:** Fleet Catalog, Route Network & Timetable Scheduling
- **Sprint Goal:** Enable bus operators to register fleet vehicles, map intercity travel routes, and publish timetable schedules.
- **Sprint Duration:** Week 2
- **Committed Points:** 13 Points
- **Completed Points:** 13 Points
- **Status:** 🟢 Completed

#### User Stories in Sprint 2:
| Story ID | Story Title | Priority | Story Points | Assignee |
|---|---|---|---|---|
| `US-03` | Bus Fleet & Seating Specifications Management | 🔴 Must Have | 5 | Archita |
| `US-04` | Route Network & Distance Definition | 🔴 Must Have | 5 | Dev Team |
| `US-05` | Bus Timetable & Dynamic Fare Scheduling | 🔴 Must Have | 3 | Dev Team |

#### Task Breakdown:
1. Create `buses`, `routes`, `schedules`, and `seats` schema in SQLite. (Owner: Dev Team, Est: 3h)
2. Implement `add_bus` with bus type and total seat validations. (Owner: Archita, Est: 3h)
3. Implement `add_route` with source/destination validations. (Owner: Dev Team, Est: 2h)
4. Implement `add_schedule` with automatic seat layout matrix generation. (Owner: Archita, Est: 4h)
5. Seed realistic fleet and intercity routes (Pune-Mumbai, Mumbai-Goa, Pune-Bangalore). (Owner: Dev Team, Est: 2h)
6. Write test cases `TC-05`, `TC-06`, `TC-07`. (Owner: Archita, Est: 2h)

- **Expected Increment:** Operable fleet management engine where operators publish departures and seats are auto-generated.
- **Actual Increment Delivered:** 100% completed.

---

### 🚀 SPRINT 3 (Week 3)
**Theme:** Bus Corridor Search, Seat Layout & Concurrency Lock
- **Sprint Goal:** Deliver passenger origin-destination search, real-time seat layout visualization, and atomic reservation with double-booking prevention.
- **Sprint Duration:** Week 3
- **Committed Points:** 16 Points
- **Completed Points:** 16 Points
- **Status:** 🟢 Completed

#### User Stories in Sprint 3:
| Story ID | Story Title | Priority | Story Points | Assignee |
|---|---|---|---|---|
| `US-06` | Search Buses by Corridor & Travel Date | 🔴 Must Have | 5 | Dev Team |
| `US-07` | Real-Time Seat Layout & Vacancy Inspection | 🔴 Must Have | 3 | Dev Team |
| `US-08` | Atomic Seat Reservation & Concurrency Lock | 🔴 Must Have | 8 | Archita |

#### Task Breakdown:
1. Implement `search_buses` with case-insensitive filters and unbooked seat counts. (Owner: Dev Team, Est: 3h)
2. Build `get_available_seats` querying seat matrix layout. (Owner: Dev Team, Est: 2h)
3. Engineer `book_ticket` with `BEGIN IMMEDIATE` transaction locking. (Owner: Archita, Est: 4h)
4. Implement defensive concurrency check rejecting conflicting bookings. (Owner: Archita, Est: 3h)
5. Add unique booking reference generator (`BK-YYYYMMDD-XXXX`). (Owner: Dev Team, Est: 2h)
6. Write test cases `TC-08`, `TC-09`, `TC-10`, `TC-11`. (Owner: Archita, Est: 3h)

- **Expected Increment:** Passengers can search buses, inspect visual seat layouts, and book seats with guaranteed concurrency locking.
- **Actual Increment Delivered:** 100% completed, zero double-booking vulnerabilities.

---

### 🚀 SPRINT 4 (Week 4)
**Theme:** Ticket Lifecycle, Cancellation & Seat Vacancy Recovery
- **Sprint Goal:** Enable self-service ticket cancellation with automatic seat vacancy recycling and passenger booking history tracking.
- **Sprint Duration:** Week 4
- **Committed Points:** 10 Points
- **Completed Points:** 10 Points
- **Status:** 🟢 Completed

#### User Stories in Sprint 4:
| Story ID | Story Title | Priority | Story Points | Assignee |
|---|---|---|---|---|
| `US-09` | Passenger Booking History & E-Ticket Details | 🟠 Should Have | 3 | Dev Team |
| `US-10` | Ticket Cancellation & Immediate Seat Recovery | 🔴 Must Have | 5 | Archita |
| `US-11` | Operator Passenger Manifest & Fleet Audit | 🟢 Could Have | 3 | Dev Team |

#### Task Breakdown:
1. Build `cancel_booking` with atomic transaction setting status to Cancelled. (Owner: Archita, Est: 3h)
2. Atomically reset `is_booked = 0` on recycled seat upon cancellation. (Owner: Archita, Est: 2h)
3. Build `get_user_bookings` returning chronological itineraries. (Owner: Dev Team, Est: 2h)
4. Implement `get_all_bookings` for operator manifest review. (Owner: Dev Team, Est: 2h)
5. Write test cases `TC-12`, `TC-13`, `TC-14`. (Owner: Archita, Est: 2h)

- **Expected Increment:** End-to-end ticket lifecycle with immediate seat recovery upon cancellation.
- **Actual Increment Delivered:** 100% completed.

---

### 🚀 SPRINT 5 (Week 5)
**Theme:** In-App Scrum Tooling, Automated Testing & Final Viva Release
- **Sprint Goal:** Integrate in-app Scrum/Kanban management, build the responsive web app, achieve 100% test coverage, and package the final release.
- **Sprint Duration:** Week 5
- **Committed Points:** 16 Points
- **Completed Points:** 16 Points
- **Status:** 🟢 Completed

#### User Stories in Sprint 5:
| Story ID | Story Title | Priority | Story Points | Assignee |
|---|---|---|---|---|
| `US-12` | In-App Scrum Backlog, Sprint & Kanban Engine | 🔴 Must Have | 8 | Archita |
| Tech-01 | Responsive Web Dashboard & HTML Kanban Board | 🟢 Could Have | 5 | Dev Team |
| Tech-02 | 16 Automated Unit & Integration Tests | 🔴 Must Have | 3 | Archita |

#### Task Breakdown:
1. Create `user_stories`, `sprints`, and `action_items` tables in SQLite. (Owner: Archita, Est: 3h)
2. Implement `KanbanService` with terminal ASCII board renderer. (Owner: Archita, Est: 3h)
3. Build standalone Python web server `app.py` with embedded REST API. (Owner: Dev Team, Est: 4h)
4. Implement `templates/index.html` and `kanban_board.html`. (Owner: Dev Team, Est: 4h)
5. Implement automated viva demonstration mode (`--demo`). (Owner: Archita, Est: 2h)
6. Write test cases `TC-15` and `TC-16`, achieving 16/16 tests passing. (Owner: Archita, Est: 2h)
7. Final academic documentation and GitHub synchronization. (Owner: Archita, Est: 3h)

- **Expected Increment:** Full dual-track system: Complete bus reservation platform + live in-app Agile Scrum/Kanban engine with 16 automated tests.
- **Actual Increment Delivered:** 100% completed and verified.

---

## 3. Sprint Velocity Summary

| Sprint | Committed Points | Completed Points | Velocity (Points) | Success Rate |
|---|---|---|---|---|
| **Sprint 1** | 6 | 6 | 6 | 100% |
| **Sprint 2** | 13 | 13 | 13 | 100% |
| **Sprint 3** | 16 | 16 | 16 | 100% |
| **Sprint 4** | 10 | 10 | 10 | 100% |
| **Sprint 5** | 16 | 16 | 16 | 100% |
| **Total** | **61** | **61** | **Avg: 12.2 pts/sprint** | **100%** |
