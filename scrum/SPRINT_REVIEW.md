# Sprint Review Reports
## Bus Booking System using Scrum Agile Methodology

---

## 1. Purpose of the Sprint Review

The **Sprint Review** is held at the conclusion of each sprint to inspect the shippable software increment delivered by the Scrum Team, demonstrate working functionality to stakeholders and the Product Owner (Archita), and adapt the Product Backlog if necessary.

---

## 2. Sprint 1 Review Report

- **Date:** Week 1, Day 7
- **Sprint Goal:** Establish SQLite database architecture and deliver secure user registration and session authentication.
- **Attendees:** Product Owner (Archita), Scrum Master, Development Team
- **Demo Agenda:**
  1. Demonstration of user account registration with unique validation.
  2. Demonstration of password hashing using SHA-256 + salt.
  3. Demonstration of user login with role session assignment (`passenger`, `operator`, `admin`).
- **User Stories Evaluated:**
  - `US-01` (Passenger & Operator Registration): Accepted 🟢 — Meets all acceptance criteria.
  - `US-02` (Credential Authentication & Role Session): Accepted 🟢 — Invalid passwords cleanly rejected.
- **Velocity Metrics:**
  - Committed Points: 6 pts | Completed Points: 6 pts | Completion: 100%
- **Stakeholder Feedback:** The authentication engine was praised for security. Recommendation made to ensure clear error messages when duplicate usernames are entered.

---

## 3. Sprint 2 Review Report

- **Date:** Week 2, Day 7
- **Sprint Goal:** Enable bus operators to register fleet vehicles, map intercity travel routes, and publish timetable schedules.
- **Attendees:** Product Owner (Archita), Scrum Master, Development Team
- **Demo Agenda:**
  1. Demonstration of bus fleet registration (Volvo, AC Sleeper, Deluxe).
  2. Demonstration of route definitions with distance and estimated travel durations.
  3. Demonstration of schedule publication and automatic generation of seat inventories.
- **User Stories Evaluated:**
  - `US-03` (Bus Fleet & Seating Capacity): Accepted 🟢
  - `US-04` (Route Network & Distance Definition): Accepted 🟢
  - `US-05` (Bus Timetable & Fare Scheduling): Accepted 🟢
- **Velocity Metrics:**
  - Committed Points: 13 pts | Completed Points: 13 pts | Completion: 100%
- **Stakeholder Feedback:** Stakeholders appreciated the automatic generation of seat records (`1A` to `6D`) upon schedule creation, removing manual seat entry errors.

---

## 4. Sprint 3 Review Report

- **Date:** Week 3, Day 7
- **Sprint Goal:** Deliver passenger origin-destination search, real-time seat layout visualization, and atomic reservation with double-booking prevention.
- **Attendees:** Product Owner (Archita), Scrum Master, Development Team
- **Demo Agenda:**
  1. Live search for Pune-Mumbai and Mumbai-Goa corridors.
  2. Live interactive seat map inspection showing open vs booked seats.
  3. Concurrent reservation test: Two users booking seat `1A` simultaneously — second user is cleanly rejected with a concurrency conflict warning.
- **User Stories Evaluated:**
  - `US-06` (Search Buses by Corridor): Accepted 🟢
  - `US-07` (Real-Time Seat Layout & Vacancy Inspection): Accepted 🟢
  - `US-08` (Atomic Ticket Booking & Concurrency Lock): Accepted 🟢
- **Velocity Metrics:**
  - Committed Points: 16 pts | Completed Points: 16 pts | Completion: 100%
- **Stakeholder Feedback:** Double-booking prevention demonstrated 100% reliability under simulation. Recommendation to generate unique human-readable ticket references (`BK-YYYYMMDD-XXXX`).

---

## 5. Sprint 4 Review Report

- **Date:** Week 4, Day 7
- **Sprint Goal:** Enable self-service ticket cancellation with automatic seat vacancy recycling and passenger booking history tracking.
- **Attendees:** Product Owner (Archita), Scrum Master, Development Team
- **Demo Agenda:**
  1. Demonstration of passenger booking history lookup.
  2. Live ticket cancellation: Booking marked `Cancelled` and seat immediately available again for new bookings.
  3. Verification that recycled seat can be reserved by another passenger.
- **User Stories Evaluated:**
  - `US-09` (Passenger Booking History): Accepted 🟢
  - `US-10` (Ticket Cancellation & Seat Recovery): Accepted 🟢
  - `US-11` (Operator Passenger Manifest): Accepted 🟢
- **Velocity Metrics:**
  - Committed Points: 10 pts | Completed Points: 10 pts | Completion: 100%
- **Stakeholder Feedback:** Immediate seat recycling praised for maximizing vehicle load factor and eliminating orphaned capacity.

---

## 6. Sprint 5 Review Report

- **Date:** Week 5, Day 7
- **Sprint Goal:** Integrate in-app Scrum/Kanban management, build responsive web application, achieve 100% test coverage, and package final viva release.
- **Attendees:** Product Owner (Archita), Scrum Master, Development Team, Academic Evaluators
- **Demo Agenda:**
  1. Execution of automated viva demonstration mode (`python src/main.py --demo`) in under 30 seconds.
  2. Live demonstration of in-app ASCII Terminal Kanban Board and Web Dashboard (`http://localhost:5000`).
  3. Execution of full 16-test automated unit test suite (`16/16 Passed, 100% Pass Rate`).
- **User Stories Evaluated:**
  - `US-12` (In-App Scrum Backlog & Kanban Engine): Accepted 🟢
  - Full project increment accepted for academic viva defense.
- **Velocity Metrics:**
  - Committed Points: 16 pts | Completed Points: 16 pts | Completion: 100%
- **Final Acceptance:** Product Owner Archita officially approved the shippable release increment.
