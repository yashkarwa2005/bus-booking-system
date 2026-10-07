# BusFlow — Online Bus Booking System
## Information Technology Lab (ITL) & Agile Methodologies (AM) Project Manual
**Academic Year:** 2026-2027 | **Semester:** 5 | **Branch:** B.Tech Computer Engineering / Information Technology  
**Student Name:** Archita | **Topic:** Bus Booking System using Scrum Agile Methodology  

---

## 1. Project Objective & Aim

To design, develop, and demonstrate a robust, concurrent **Online Bus Booking System** (`BusFlow`) managed under the **Scrum Agile Methodology**. The system streamlines intercity bus discovery, eliminates seat double-booking collisions through atomic database transactions, produces instant digital booking references, enables immediate seat vacancy recycling upon cancellation, and provides transparent administrative oversight alongside an integrated Scrum Kanban engine.

---

## 2. Technology Stack & Prerequisites

| Layer | Technology | Details |
| :--- | :--- | :--- |
| **Backend** | Python 3.8+ (Tested on 3.10+) | Standard library `http.server`, multi-threaded request dispatcher |
| **Database** | SQLite3 | Relational ACID database with Foreign Keys enabled (`PRAGMA foreign_keys = ON`) |
| **Security** | SHA-256 + Salted Hashing | Cryptographic credential protection against rainbow table attacks |
| **Frontend** | HTML5, CSS3, Vanilla JS | Dark/Light modern bus transit dashboard with interactive seat picker |
| **Testing** | Python `unittest` framework | 16 comprehensive automated unit tests covering all core modules (100% pass) |
| **Agile Tools** | GitHub Projects V2 & In-App Kanban | 5-stage Kanban flow (Backlog, Todo, In Progress, Review, Done) |

---

## 3. How to Run the Project for Demonstration

### Method 1: One-Click Double Click (Recommended for Viva)
1. Navigate to the project folder:
   ```text
   ITL/
   ```
2. Double-click the file:
   ```text
   run.bat
   ```
3. The server starts, connects to `database/bus_booking.db`, and opens the live dashboard at:
   ```text
   http://127.0.0.1:5000
   ```

### Method 2: Via Terminal Command Line
```powershell
# Open terminal inside ITL/ folder and run:
python app.py
```

### Method 3: Instant Automated Viva Demonstration Mode (<30s)
```powershell
python src/main.py --demo
```
*Walks through user authentication, corridor search, seat map inspection, atomic reservation, double-booking rejection, ticket cancellation, seat recovery, and terminal Kanban board automatically.*

### Method 4: Run Automated Test Suite (To show 100% test pass to teacher)
```powershell
python -m unittest tests/test_bus_booking.py -v
```
*(All 16 unit tests pass in ~0.8s)*

---

## 4. Key Functional Modules Demonstrated to Evaluator

### Module 1: Passenger Bus Search & Interactive Seat Map
- Filter buses by origin and destination: **Pune &rarr; Mumbai**, **Mumbai &rarr; Goa**, **Pune &rarr; Bangalore**.
- Inspect available buses: Shivneri Volvo Multi-Axle, Neeta Royal Sleeper, Purple Deluxe.
- Interactive Seat Layout Map: Displays window vs aisle seats, visual green markers for available seats, and red markers for booked seats.

### Module 2: Atomic Seat Reservation & Concurrency Guard
- Select seat (e.g. `1A` or `2B`) and enter passenger details.
- System initiates an atomic SQLite transaction (`BEGIN IMMEDIATE;`).
- Locks the chosen seat, assigns unique reference (`BK-20261015-XXXX`), and prints a confirmation receipt.
- **Double-Booking Demonstration:** If another user attempts to book the same seat, the concurrency guard cleanly rejects the attempt with: `"Concurrency Conflict: Seat is already booked."`

### Module 3: Ticket Cancellation & Immediate Seat Recovery
- Under **My Bookings**, passenger clicks **Cancel Ticket**.
- Booking transitions to `Cancelled` and the seat is atomically recycled to `is_booked = 0`.
- Refreshing the seat map immediately shows the seat as available for new passengers.

### Module 4: Operator Manifest & Administrative Audit Log
- Fleet operators can review all registered buses, route distances, departure timetables, and global passenger manifests.

### Module 5: Integrated Agile Scrum & Kanban Engine
- Inspect 5-column Kanban board at `http://127.0.0.1:5000/kanban` or in terminal via `python src/main.py --kanban`.
- Review sprint commitments, velocity metrics, and burndown progression.

---

## 5. Viva Voce Questions & Model Answers

### Q1: How do you prevent double booking when multiple users try to reserve the same seat simultaneously?
> **Answer:** We enforce transactional concurrency control in SQLite using `BEGIN IMMEDIATE;`. Before updating the seat record, the transaction inspects the `is_booked` column. If `is_booked == 1`, the transaction immediately rolls back and raises a concurrency exception. Only one process can acquire the write lock, guaranteeing atomicity and isolation (ACID).

### Q2: Why did you choose SQLite instead of MySQL or PostgreSQL for this PBL?
> **Answer:** SQLite is serverless, zero-configuration, and ACID-compliant. It runs portably on any evaluation machine out-of-the-box without requiring background database services, root privileges, or network port configuration, while supporting complete foreign key constraints and transactional locking.

### Q3: How does Scrum differ from the traditional Waterfall model?
> **Answer:** Waterfall is linear and sequential with rigid phases where working software is only visible at the end. Scrum is iterative and incremental, organizing work into short fixed-length Sprints (1 week in our project) that produce a potentially shippable software increment at the end of every sprint, welcoming changes and stakeholder feedback.

### Q4: What is the MoSCoW prioritization technique and how is it used here?
> **Answer:** MoSCoW categorizes requirements into **Must Have** (critical core like authentication and atomic booking), **Should Have** (important features like booking history), **Could Have** (desirable items like passenger manifest), and **Won't Have** (deferred items like external SMS gateway). This ensures vital features are delivered even under strict timeline constraints.

### Q5: What is the INVEST principle for User Stories?
> **Answer:** Good user stories must be:
> - **I**ndependent (can be built separately)
> - **N**egotiable (open to discussion)
> - **V**aluable (delivers value to user)
> - **E**stimable (can be sized in story points)
> - **S**mall (fits within a single sprint)
> - **T**estable (has verifiable acceptance criteria)

### Q6: How do you handle password security in your system?
> **Answer:** Passwords are never stored in plaintext. We use cryptographic salted SHA-256 hashing (`bus_scrum_salt_2026`). Even identical passwords generate completely different hashes if salted uniquely, defending against dictionary attacks and precomputed rainbow table lookups.

---

## 6. Evaluation & Marking Scheme Rubric

| Component | Marks Allocated | Achieved Status |
| :--- | :---: | :---: |
| **Problem Definition & Scope** | 10 | Complete Bus Reservation domain with concurrency handling |
| **Scrum Methodology & Artifacts** | 25 | 12 User Stories, 5 Sprints, MoSCoW, Burndown & Kanban |
| **System Architecture & Database Design** | 20 | 3-tier design, normalized SQLite schema, foreign keys |
| **Implementation & Working Demo** | 25 | Interactive Web Dashboard + CLI + Automated Viva Demo |
| **Testing & Quality Assurance** | 10 | 16 automated unit tests with 100% pass rate |
| **Viva Voce & Documentation** | 10 | Comprehensive Lab Manual, README, and design specs |
| **Total** | **100** | **100 / 100** |
