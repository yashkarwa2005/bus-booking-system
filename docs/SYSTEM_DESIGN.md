# System Design & Architecture
## Bus Booking System using Scrum Agile Methodology

---

## 1. System Architecture

The project is architected following a modular **3-Tier Layered Architecture**, separating user presentation, business rules, and persistent data storage.

```mermaid
graph TD
    subgraph Presentation_Layer [Presentation Layer / CLI & Web]
        CLI[Interactive Terminal UI - main.py]
        KanbanRenderer[Terminal ASCII Kanban - kanban.py]
        DemoEngine[Automated Viva Demo Engine --demo]
        WebServer[HTTP Server & REST API - app.py]
        WebUI[HTML5 / CSS3 Dashboard - index.html]
    end

    subgraph Service_Layer [Service & Business Logic Layer]
        BusService[Bus Booking Service - bus_booking.py]
        StoryService[User Story Service - user_story.py]
        SprintService[Sprint Service - sprint.py]
        ActionService[Action Item Service - action_item.py]
    end

    subgraph Data_Layer [Data & Persistence Layer]
        DBManager[Database Module - database.py]
        SQLiteDB[(SQLite Database - bus_booking.db)]
    end

    CLI --> BusService
    CLI --> StoryService
    CLI --> SprintService
    CLI --> ActionService
    CLI --> KanbanRenderer
    DemoEngine --> BusService
    DemoEngine --> KanbanRenderer

    WebServer --> BusService
    WebServer --> StoryService
    WebServer --> SprintService
    WebServer --> ActionService
    WebUI --> WebServer

    BusService --> DBManager
    StoryService --> DBManager
    SprintService --> DBManager
    ActionService --> DBManager

    DBManager --> SQLiteDB
```

---

## 2. Database Design & Entity-Relationship Diagram (ERD)

The system utilizes an embedded relational database (SQLite 3) with strict foreign key constraints enabled via `PRAGMA foreign_keys = ON;`.

```mermaid
erDiagram
    USERS ||--o{ BUSES : "operates"
    USERS ||--o{ BOOKINGS : "places"
    BUSES ||--o{ SCHEDULES : "assigned to"
    ROUTES ||--o{ SCHEDULES : "traversed by"
    SCHEDULES ||--o{ SEATS : "contains"
    SCHEDULES ||--o{ BOOKINGS : "reserves on"
    SEATS ||--o| BOOKINGS : "allocated to"
    SPRINTS ||--o{ USER_STORIES : "contains"
    SPRINTS ||--o{ ACTION_ITEMS : "tracks"
```

---

## 3. Concurrency Lock Sequence Diagram (Atomic Seat Booking)

This sequence diagram illustrates how `US-08` achieves zero double-booking concurrency collisions using SQLite atomic transactions.

```mermaid
sequenceDiagram
    autonumber
    actor Passenger1 as Passenger A
    actor Passenger2 as Passenger B
    participant Service as BusBookingService
    participant DB as SQLite bus_booking.db

    Passenger1->>Service: book_ticket(schedule_id=1, seat='1A')
    Service->>DB: BEGIN IMMEDIATE TRANSACTION
    Service->>DB: SELECT is_booked FROM seats WHERE seat_number='1A'
    DB-->>Service: is_booked = 0 (Vacant)
    
    par Concurrent Request
        Passenger2->>Service: book_ticket(schedule_id=1, seat='1A')
        Service->>DB: BEGIN IMMEDIATE TRANSACTION (Waits / Locked)
    end

    Service->>DB: UPDATE seats SET is_booked = 1 WHERE seat_number='1A'
    Service->>DB: INSERT INTO bookings (ref, seat_number, status='Confirmed')
    Service->>DB: COMMIT TRANSACTION
    DB-->>Service: Transaction Committed
    Service-->>Passenger1: Booking Confirmed (BK-20261015-8492)

    Note over Service,DB: Passenger B's transaction resumes
    Service->>DB: SELECT is_booked FROM seats WHERE seat_number='1A'
    DB-->>Service: is_booked = 1 (Already Booked!)
    Service->>DB: ROLLBACK TRANSACTION
    Service-->>Passenger2: Error: Concurrency Conflict: Seat '1A' is already booked.
```

---

## 4. Ticket Cancellation & Immediate Seat Recovery Sequence

```mermaid
sequenceDiagram
    autonumber
    actor Passenger as Passenger
    participant Service as BusBookingService
    participant DB as SQLite bus_booking.db

    Passenger->>Service: cancel_booking(booking_id=1)
    Service->>DB: BEGIN IMMEDIATE TRANSACTION
    Service->>DB: SELECT * FROM bookings WHERE id=1
    DB-->>Service: booking (status='Confirmed', seat_id=10)
    Service->>DB: UPDATE bookings SET status='Cancelled' WHERE id=1
    Service->>DB: UPDATE seats SET is_booked=0 WHERE id=10
    Service->>DB: INSERT INTO audit_logs ('TICKET_CANCELLED')
    Service->>DB: COMMIT TRANSACTION
    Service-->>Passenger: Success: Booking cancelled and seat recycled.
```

---

## 5. Security & Data Integrity Controls

1. **Cryptographic Protection:** Passwords are hashed using salted SHA-256 (`bus_scrum_salt_2026`), protecting against dictionary attacks and rainbow tables.
2. **Defensive Concurrency Guard:** The `book_ticket` method executes within an explicit `BEGIN IMMEDIATE;` block, checking seat status before applying modifications.
3. **Role-Based Access Control:** Differentiates `passenger`, `operator`, and `admin` permissions.
4. **Audit Logging:** All critical business events (`TICKET_BOOKED`, `TICKET_CANCELLED`, `SYSTEM_INIT`) are persisted in `audit_logs` for transparency.
