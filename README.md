# Bus Booking System using Scrum Agile Methodology

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)](https://www.sqlite.org/)
[![Agile Methodology](https://img.shields.io/badge/Methodology-Scrum%20%2F%20Kanban-success.svg)](https://www.scrum.org/)
[![Tests](https://img.shields.io/badge/Unit%20Tests-16%20Passed%20(100%25)-brightgreen.svg)](tests/test_bus_booking.py)
[![License](https://img.shields.io/badge/License-Academic%20PBL-orange.svg)](#)

> **B.Tech 3rd-Year Project-Based Learning (PBL) Submission**  
> **Course:** Agile Methodologies & IT (AM)  
> **Author / Scrum Lead:** Archita  
> **Repository:** [yashkarwa2005/bus-booking-system](https://github.com/yashkarwa2005/bus-booking-system.git)

---

## 1. Project Overview

The **Bus Booking System** is an end-to-end, domain-driven software solution engineered to streamline intercity bus discovery, eliminate seat double-booking concurrency conflicts, and deliver transparent seat map availability for both passengers and bus fleet operators.

More importantly, the entire development lifecycle serves as a practical demonstration of **Scrum Agile Methodology**. To satisfy the B.Tech Agile Methodologies curriculum, the delivered codebase features a **dual-track architecture**:
1. **Bus Reservation Engine:** User authentication, origin-destination corridor search, dynamic seat layout visualization (window vs aisle), atomic reservation locking, self-service cancellation, and automatic seat vacancy recovery.
2. **Built-in Scrum & Kanban Management Engine:** Persistent SQLite tables for user stories, sprint lifecycles, action items, an interactive terminal ASCII Kanban board, and a responsive web dashboard.

---

## 2. Problem Statement

Traditional bus booking platforms and manual ticketing workflows suffer from three critical bottlenecks:
- **Double-Booking & Schedule Collisions:** Lack of transactional concurrency locks results in multiple passengers reserving the same physical seat during simultaneous booking attempts.
- **Stranded Capacity on Cancellations:** When passengers cancel journeys late, open seats frequently remain orphaned rather than immediately recycling into available inventory for other travelers.
- **Fragmented Visibility:** Passengers lack clear seat map previews (window vs aisle), and fleet operators struggle to maintain accurate departure manifests.

From a software engineering perspective, projects often fail due to monolithic waterfall planning, lack of iteration transparency, and scope creep. This project solves both the transportation domain problem and the software project management problem through disciplined 5-week Scrum iterations.

---

## 3. Project Objectives

- **Zero Concurrency Collisions:** Enforce atomic database transactions (`BEGIN IMMEDIATE`) to guarantee that no bus seat can ever be double-booked.
- **Full Lifecycle Management:** Enable self-service registration, corridor search, seat selection, booking, cancellation with automatic seat vacancy recycling, and passenger history tracking.
- **Authentic Scrum Execution:** Practice all Scrum roles, ceremonies, artifacts, INVEST-compliant user stories, and Gherkin-formatted acceptance criteria.
- **In-App Agile Tooling:** Integrate real-time Kanban visualization and backlog metrics directly inside the Python console and web dashboard.
- **Zero Third-Party Hurdles:** Implement using pure Python standard libraries (`sqlite3`, `hashlib`, `unittest`, `http.server`) to run out-of-the-box on any evaluation machine.

For detailed curriculum mapping and academic objectives, see [docs/PROJECT_OBJECTIVES.md](docs/PROJECT_OBJECTIVES.md).

---

## 4. Key Features

### 🚍 Bus Reservation Subsystem
- **Salted SHA-256 Authentication:** Secure registration and login for passengers, bus operators, and system administrators.
- **Fleet & Route Directory:** Operator management for buses (Volvo Multi-Axle, AC Sleeper, Deluxe) and travel corridors (Pune-Mumbai, Mumbai-Goa, Pune-Bangalore).
- **Corridor Timetable Search:** Fast search by origin, destination, and departure date.
- **Interactive Seat Map:** Visual matrix of booked vs available seats distinguishing window and aisle positions.
- **Atomic Concurrency Lock:** Immediate seat locking with defensive validation rejecting simultaneous booking collisions.
- **Self-Service Cancellation:** Atomically updates booking status to `Cancelled` and immediately recycles the seat (`is_booked = 0`).
- **Passenger History & Manifest:** Chronological itinerary history for passengers and global audit manifest for fleet managers.

### 📊 Scrum Project Management Subsystem
- **Interactive Terminal Kanban Board:** 5-column ASCII board (`Backlog -> To Do -> In Progress -> Review/Testing -> Done`) with task cards, story points, and priority badges.
- **Responsive Web Dashboard (`http://localhost:5000`):** Standalone browser dashboard with live seat map picker, booking receipts, and drag-and-drop web Kanban board (`/kanban`).
- **Product Backlog Management:** Full tracking of 12 user stories with MoSCoW prioritization and Fibonacci estimation.
- **5-Week Sprint Cadence:** Sprint goal tracking, committed vs completed points, and velocity calculations.
- **Action Item Register:** Weekly impediment and task tracking with ownership and statuses.
- **Instant Automated Viva Demo (`--demo`):** Automated walkthrough executing all core features and Agile validation in under 30 seconds.

---

## 5. Technology Stack

| Component | Technology | Rationale |
|---|---|---|
| **Programming Language** | Python 3.8+ (Tested on 3.10+) | Clean, readable syntax; standard in enterprise and academia. |
| **Persistence / Database** | SQLite 3 (`sqlite3`) | Zero-configuration relational database with ACID compliance and foreign key enforcement. |
| **Cryptography** | `hashlib` (SHA-256 + Salt) | Secure password storage defending against rainbow tables. |
| **Testing Framework** | `unittest` | Built-in unit and integration test runner requiring zero pip packages. |
| **Web Server & REST API** | `http.server` & `json` | Built-in HTTP server providing embedded REST API without external framework overhead. |
| **User Interface** | ANSI Console & Modern HTML5/CSS3 | Portable CLI with color badges plus modern responsive web portal. |
| **Version Control** | Git & GitHub | Distributed version control, milestone planning, and release tracking. |

---

## 6. Scrum Methodology Implementation

The project strictly follows the Scrum Framework as defined in the Scrum Guide:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SCRUM METHODOLOGY CADENCE                          │
└─────────────────────────────────────────────────────────────────────────────┘
  Product Vision ──> Product Backlog (Refined & Estimated via Planning Poker)
                            │
                            ▼
                     Sprint Planning (Commitment & Goal Definition)
                            │
                            ▼
               Sprint Execution (Weekly Sprints 1 to 5)
                 ├── Daily Scrum & Impediment Removal
                 └── Kanban Flow (WIP Limits, Column Progression)
                            │
                            ▼
                     Sprint Review (Increment Demonstration & Stakeholder Feedback)
                            │
                            ▼
                     Sprint Retrospective (Continuous Team Improvement)
                            │
                            ▼
               Potentially Shippable Product Increment
```

### Scrum Team Roles & Responsibilities:
- **Product Owner (Archita):** Defined the product vision, authored user stories, maintained MoSCoW priorities, and accepted completed increments against Acceptance Criteria.
- **Scrum Master:** Facilitated sprint planning, daily standups, sprint reviews, and retrospectives; removed technical impediments.
- **Development Team (Led by Archita):** Engineered database schema, transactional booking algorithms, CLI console, web dashboard, and automated test cases.

---

## 7. Requirement Prioritization (MoSCoW)

- 🔴 **MUST HAVE (35 Story Points):** User Registration, Authentication, Bus Fleet Management, Route Mapping, Timetable Scheduling, Corridor Bus Search, Dynamic Seat Map, Atomic Seat Booking Lock, Ticket Cancellation with Seat Recycling.
- 🟠 **SHOULD HAVE (6 Story Points):** Passenger Booking History, In-App Scrum Backlog & Kanban Engine.
- 🟢 **COULD HAVE (8 Story Points):** Operator Passenger Manifest & Fleet Audit, Web Live Kanban Dashboard.
- ⚪ **WON'T HAVE (Deferred):** Third-party online payment gateway, automated carrier SMS gateway, real-time GPS hardware telematics.

Full MoSCoW breakdown: [scrum/REQUIREMENT_PRIORITIES.md](scrum/REQUIREMENT_PRIORITIES.md)

---

## 8. 5-Week Sprint Overview

The project was executed across five structured 1-week sprint iterations:

| Sprint | Theme / Milestone | Committed | Completed | Velocity | Status |
|---|---|---|---|---|---|
| **Sprint 1** | Identity, Authentication & Core Architecture | 6 pts | 6 pts | 6 pts | 🟢 Completed |
| **Sprint 2** | Bus Fleet, Route Network & Timetables | 13 pts | 13 pts | 13 pts | 🟢 Completed |
| **Sprint 3** | Corridor Search, Seat Layout & Atomic Lock | 16 pts | 16 pts | 16 pts | 🟢 Completed |
| **Sprint 4** | Ticket Lifecycle, Cancellation & Seat Recovery | 10 pts | 10 pts | 10 pts | 🟢 Completed |
| **Sprint 5** | In-App Scrum Tooling, Automated Testing & Release | 16 pts | 16 pts | 16 pts | 🟢 Completed |
| **Total** | **5 Sprints** | **61 pts** | **61 pts** | **Avg: 12.2 pts/sprint** | **100% Success** |

Detailed sprint plans: [scrum/SPRINT_PLAN.md](scrum/SPRINT_PLAN.md)

---

## 9. Product Backlog & User Stories

| Story ID | Story Title | Role | Priority | Story Points | Sprint | Status | Assignee |
|---|---|---|---|---|---|---|---|
| `US-01` | Passenger & Operator Registration | Passenger | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done | Archita |
| `US-02` | Credential Authentication & Role Session | All Roles | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done | Dev Team |
| `US-03` | Bus Fleet & Capacity Management | Operator | 🔴 Must Have | 5 | Sprint 2 | 🟢 Done | Archita |
| `US-04` | Route Network & Distance Definition | Operator | 🔴 Must Have | 5 | Sprint 2 | 🟢 Done | Dev Team |
| `US-05` | Bus Timetable & Dynamic Fare Scheduling | Operator | 🔴 Must Have | 3 | Sprint 2 | 🟢 Done | Dev Team |
| `US-06` | Search Buses by Corridor & Travel Date | Passenger | 🔴 Must Have | 5 | Sprint 3 | 🟢 Done | Dev Team |
| `US-07` | Real-Time Seat Layout & Vacancy Inspection | Passenger | 🔴 Must Have | 3 | Sprint 3 | 🟢 Done | Dev Team |
| `US-08` | Atomic Seat Reservation & Concurrency Lock | Passenger | 🔴 Must Have | 8 | Sprint 3 | 🟢 Done | Archita |
| `US-09` | Passenger Booking History & E-Ticket Details | Passenger | 🟠 Should Have | 3 | Sprint 4 | 🟢 Done | Dev Team |
| `US-10` | Ticket Cancellation & Immediate Seat Recovery | Passenger | 🔴 Must Have | 5 | Sprint 4 | 🟢 Done | Archita |
| `US-11` | Operator Passenger Manifest & Fleet Audit | Operator | 🟢 Could Have | 3 | Sprint 5 | 🟢 Done | Dev Team |
| `US-12` | In-App Scrum Backlog, Sprint & Kanban Engine | Scrum Team | 🔴 Must Have | 8 | Sprint 5 | 🟢 Done | Archita |

Detailed specifications:
- [readme/USER_STORY.md](readme/USER_STORY.md)
- [readme/ACCEPTANCE_CRITERIA.md](readme/ACCEPTANCE_CRITERIA.md)

---

## 10. Kanban Board & Visual Workflow

The project tracks task progression across 5 visual stages:

```text
📋 BACKLOG ──> 🔵 TO DO ──> 🟡 IN PROGRESS ──> 🟣 REVIEW/TESTING ──> 🟢 DONE
```

To view the live Kanban board:
- **Terminal Display:** `python src/main.py --kanban`
- **Interactive Web Board:** Start `python app.py` and navigate to [http://localhost:5000/kanban](http://localhost:5000/kanban)
- **Documentation Board:** [scrum/KANBAN_BOARD.md](scrum/KANBAN_BOARD.md)

---

## 11. Project Directory Structure

```text
bus-booking-system/
│
├── README.md                           # Master Project Documentation & Evaluation Guide
├── app.py                              # Standalone Python Web Application & REST API
├── kanban_board.html                   # Interactive Browser Kanban Board
├── requirements.txt                    # Environment dependencies (Zero mandatory packages)
├── run.bat                             # One-click Windows launch script
├── .gitignore                          # Git ignore rules for Python & SQLite
│
├── src/                                # Core Application Source Code
│   ├── __init__.py                     # Package marker
│   ├── database.py                     # SQLite schema, foreign keys & seed data
│   ├── bus_booking.py                  # Bus booking engine, concurrency locks & cancellation
│   ├── user_story.py                   # Scrum User Story service
│   ├── sprint.py                       # Sprint planning & velocity metrics
│   ├── action_item.py                  # Action items & impediment tracker
│   ├── kanban.py                       # Terminal ASCII Kanban renderer
│   └── main.py                         # Interactive CLI & Automated Viva Demo
│
├── templates/                          # Web Presentation Templates
│   └── index.html                      # Responsive Bus Booking Web Dashboard
│
├── tests/                              # Automated Test Suite
│   ├── __init__.py                     # Package marker
│   └── test_bus_booking.py             # 16 automated unit & integration test cases
│
├── readme/                             # Agile Specifications
│   ├── USER_STORY.md                   # 12 INVEST user stories with personas
│   └── ACCEPTANCE_CRITERIA.md          # Gherkin-formatted acceptance criteria
│
├── scrum/                              # Scrum Ceremonies & Governance Artifacts
│   ├── PRODUCT_BACKLOG.md              # Ranked product backlog & refinement logs
│   ├── REQUIREMENT_PRIORITIES.md       # MoSCoW prioritization & justification
│   ├── SPRINT_PLAN.md                  # 5-week sprint iteration breakdown & tasks
│   ├── KANBAN_BOARD.md                 # 5-column Kanban board markdown
│   ├── ACTION_ITEMS.md                 # 18 weekly action items with owners & dates
│   ├── SPRINT_REVIEW.md                # Sprint review meeting records & feedback
│   └── SPRINT_RETROSPECTIVE.md         # Continuous improvement retrospectives
│
├── docs/                               # Academic & Architectural Documentation
│   ├── PROJECT_OBJECTIVES.md           # Syllabus mapping & course objectives
│   ├── SYSTEM_DESIGN.md                # 3-tier architecture, ERD & sequence diagrams
│   └── TESTING.md                      # Test strategy, execution report & RTM
│
└── scripts/                            # Automation & Synchronization Scripts
    ├── populate_github_issues.py       # REST API populator for GitHub Issues & Milestones
    └── clean_github_issues.py          # GitHub issue label & status synchronizer
```

---

## 12. Installation & Setup

### Prerequisites
- Python 3.8 or higher installed on your machine ([Download Python](https://www.python.org/downloads/)).
- Git installed on your system.

### Step 1: Clone the Repository
```bash
git clone https://github.com/yashkarwa2005/bus-booking-system.git
cd bus-booking-system
```

### Step 2: (Optional) Install Dependencies
The application runs out of the box with zero external packages. For optional enhanced terminal formatting:
```bash
pip install -r requirements.txt
```

---

## 13. Running the Application

### Option A: Instant Automated Viva Demonstration Mode (Recommended for Viva)
Walk through all Agile user stories, search, seat map inspection, atomic reservation, double-booking rejection, ticket cancellation, seat recovery, and live Kanban board automatically in under 30 seconds:
```bash
python src/main.py --demo
```

### Option B: Interactive Terminal Console
Launch the full interactive command-line menu:
```bash
python src/main.py
```
Pre-seeded accounts for immediate testing:
- **Passenger Account:** Username: `archita_p` | Password: `archita123`
- **Operator Account:**  Username: `operator_neeta` | Password: `operator123`
- **Admin Account:**     Username: `admin` | Password: `admin123`

### Option C: Direct Terminal Kanban Board Display
Display the live SQLite-driven ASCII Kanban board directly:
```bash
python src/main.py --kanban
```

### Option D: Standalone Web Server & Interactive Dashboard
Start the local HTTP server:
```bash
python app.py
```
Then open your browser at:
- **Bus Booking Portal:** [http://localhost:5000](http://localhost:5000)
- **Live Scrum Kanban Board:** [http://localhost:5000/kanban](http://localhost:5000/kanban)

---

## 14. Automated Testing & Verification

The project includes an automated test suite with **16 test cases** covering every layer of the architecture:

```bash
python -m unittest tests/test_bus_booking.py -v
```

### Test Results:
- **Total Test Cases:** 16
- **Passed:** 16 (100%)
- **Failed:** 0
- **Execution Time:** ~1.1s
- **Traceability Report:** [docs/TESTING.md](docs/TESTING.md)

---

## 15. Student & Submission Information

- **Student Name:** Archita
- **Degree:** B.Tech (3rd Year, Semester 5)
- **Course:** Agile Methodologies & IT (AM)
- **Destination GitHub Repository:** [yashkarwa2005/bus-booking-system](https://github.com/yashkarwa2005/bus-booking-system.git)
- **Evaluation Status:** 100% Completed, Verified & Shippable
