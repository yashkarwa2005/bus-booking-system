# Acceptance Criteria Documentation
## Bus Booking System using Scrum Agile Methodology

---

## 1. What are Acceptance Criteria?

In Scrum and Agile software engineering, **Acceptance Criteria (AC)** are the formal, predetermined conditions that a software product or user story must satisfy to be accepted by the Product Owner, stakeholders, and end users.

### Purpose of Acceptance Criteria
1. **Defines Boundaries:** Clearly marks the scope of a user story, preventing scope creep.
2. **Establishes Consensus:** Aligns the Product Owner and Development Team on what "completed" means.
3. **Forms the Basis for Testing:** Translates directly into automated unit, integration, and system test cases.
4. **Supports the Definition of Done (DoD):** A user story cannot transition to `Done` until 100% of its acceptance criteria pass automated verification.

---

## 2. Reusable Gherkin Template

```gherkin
Scenario: [Title of scenario]
Given [Initial context / precondition]
When [Action triggered by the user or system]
Then [Expected outcome / postcondition]
And [Additional condition or side-effect]
```

---

## 3. Detailed Acceptance Criteria for User Stories

---

### AC-US01: Passenger & Operator Registration
**Linked Story:** [US-01: Passenger & Operator Registration](USER_STORY.md#us-01-passenger--operator-registration)

#### Scenario 1: Successful passenger account registration
- **Given** an unregistered traveler accesses the registration module,
- **When** the traveler enters a valid username (`priya_sharma`), secure password (`SecurePass@123`), full name (`Priya Sharma`), email (`priya.sharma@example.com`), phone (`9811223344`), and role `passenger`,
- **Then** the system hashes the password using salted SHA-256,
- **And** inserts the new record into the `users` SQLite table,
- **And** returns a positive confirmation with a generated user ID.

#### Scenario 2: Duplicate username or email rejection
- **Given** an existing user is already registered with username `archita_p`,
- **When** a new user attempts to register with `archita_p`,
- **Then** the system detects the unique constraint conflict,
- **And** aborts the operation with a clear error: `"Username or Email is already registered."`.

#### Scenario 3: Validation of mandatory input fields
- **Given** a user leaves mandatory fields blank (e.g. empty password or username),
- **When** registration submission occurs,
- **Then** the service raises a `ValueError` rejecting the incomplete submission.

---

### AC-US02: Credential Authentication & Role Session
**Linked Story:** [US-02: Credential Authentication & Role Session](USER_STORY.md#us-02-credential-authentication--role-session)

#### Scenario 1: Successful login with valid credentials
- **Given** a registered user with username `archita_p` and password `archita123`,
- **When** the user submits these credentials,
- **Then** the service computes the salted SHA-256 hash, verifies the match against the database,
- **And** returns an authenticated session containing `id`, `username`, `full_name`, and `role`.

#### Scenario 2: Rejection of invalid password or non-existent username
- **Given** a user enters an incorrect password or an unregistered username,
- **When** login is evaluated,
- **Then** authentication fails with `"Invalid username or password."`,
- **And** no active session is created.

---

### AC-US03: Bus Fleet Management
**Linked Story:** [US-03: Bus Fleet & Seating Capacity Management](USER_STORY.md#us-03-bus-fleet-management)

#### Scenario 1: Operator registers new bus
- **Given** an authorized bus operator,
- **When** the operator submits bus number `MH-12-RN-4501`, name `Shivneri Volvo Multi-Axle`, type `Volvo Multi-Axle`, and capacity `24`,
- **Then** the system validates the bus type against permitted categories,
- **And** inserts the record into `buses` with primary key `id`.

#### Scenario 2: Duplicate bus registration number prevention
- **Given** a bus with number `MH-12-RN-4501` is already registered,
- **When** an operator attempts to register the same bus number again,
- **Then** the system aborts with a unique constraint violation error.

---

### AC-US04: Intercity Route Mapping
**Linked Story:** [US-04: Intercity Route & Distance Mapping](USER_STORY.md#us-04-intercity-route-mapping)

#### Scenario 1: Creating a valid intercity corridor
- **Given** valid origin `Pune` and destination `Mumbai` with distance `150.0 km` and duration `3.5 hours`,
- **When** the route is submitted,
- **Then** the system stores the corridor in `routes`.

#### Scenario 2: Rejection of identical origin and destination
- **Given** an operator inputs source `Pune` and destination `Pune`,
- **When** submission occurs,
- **Then** the system raises a `ValueError` indicating origin and destination cannot be identical.

---

### AC-US05: Bus Timetable & Fare Scheduling
**Linked Story:** [US-05: Bus Timetable & Dynamic Fare Scheduling](USER_STORY.md#us-05-bus-timetable--fare-scheduling)

#### Scenario 1: Publishing a departure schedule with auto-generated seats
- **Given** existing bus ID `1` (capacity 24) and route ID `1`,
- **When** an operator publishes a schedule for `2026-10-15` departing at `06:00 AM` with fare `650.0`,
- **Then** the schedule record is inserted into `schedules`,
- **And** 24 seat records (`1A` to `6D`) are automatically populated into `seats` with `is_booked = 0`.

---

### AC-US06: Search Buses by Corridor
**Linked Story:** [US-06: Search Buses by Corridor & Travel Date](USER_STORY.md#us-06-search-buses-by-corridor)

#### Scenario 1: Finding available buses between cities
- **Given** active schedules connecting `Pune` and `Mumbai`,
- **When** a passenger searches with origin `Pune` and destination `Mumbai`,
- **Then** the system returns matching schedules showing bus name, departure time, fare, and count of unbooked seats.

---

### AC-US07: Seat Layout & Vacancy Inspection
**Linked Story:** [US-07: Real-Time Seat Layout & Vacancy Inspection](USER_STORY.md#us-07-seat-layout--vacancy-inspection)

#### Scenario 1: Querying seat layout matrix
- **Given** schedule ID `1` with seats `1A` booked and `1B` unbooked,
- **When** a passenger views the seat layout for schedule `1`,
- **Then** the system returns all seats with their layout coordinates, seat type (Window/Aisle), and `is_booked` indicator.

---

### AC-US08: Atomic Ticket Booking & Concurrency Lock
**Linked Story:** [US-08: Atomic Ticket Booking & Concurrency Lock](USER_STORY.md#us-08-atomic-ticket-booking--concurrency-lock)

#### Scenario 1: Successful atomic seat reservation
- **Given** seat `1B` is vacant on schedule `1`,
- **When** passenger `Archita` confirms booking for seat `1B`,
- **Then** the system starts an immediate SQLite transaction,
- **And** sets `is_booked = 1` for seat `1B`,
- **And** creates a booking record with a unique reference formatted as `BK-YYYYMMDD-XXXX`,
- **And** commits the transaction.

#### Scenario 2: Prevention of duplicate / double-booking (Race condition)
- **Given** seat `1A` is already booked (`is_booked = 1`),
- **When** another passenger attempts to book seat `1A`,
- **Then** the concurrency check detects the lock,
- **And** rolls back the transaction,
- **And** raises an exception: `"Concurrency Conflict: Seat '1A' is already booked."`.

---

### AC-US09: Passenger Booking History
**Linked Story:** [US-09: Passenger Booking History & E-Ticket Details](USER_STORY.md#us-09-passenger-booking-history)

#### Scenario 1: Viewing personalized travel bookings
- **Given** an authenticated passenger with past and current reservations,
- **When** the passenger requests booking history,
- **Then** the system returns all reservations belonging to that user ID ordered chronologically, showing reference, seat, route, fare, and status.

---

### AC-US10: Ticket Cancellation & Seat Recovery
**Linked Story:** [US-10: Ticket Cancellation & Immediate Seat Recovery](USER_STORY.md#us-10-ticket-cancellation--seat-recovery)

#### Scenario 1: Cancelling confirmed ticket and recycling seat vacancy
- **Given** confirmed booking `#1` for seat `1A` on schedule `1`,
- **When** the passenger cancels the booking,
- **Then** the booking status transitions to `Cancelled`,
- **And** seat `1A` on schedule `1` is updated atomically to `is_booked = 0`,
- **And** subsequent seat searches immediately show seat `1A` as available for booking.

---

### AC-US11: Operator Passenger Manifest
**Linked Story:** [US-11: Operator Passenger Manifest & Fleet Audit](USER_STORY.md#us-11-operator-passenger-manifest)

#### Scenario 1: Administrative manifest review
- **Given** administrative or fleet operator privileges,
- **When** the operator opens the global manifest,
- **Then** the system displays all bookings across all routes and buses with passenger names, ages, and seat assignments.

---

### AC-US12: In-App Scrum Backlog & Kanban Engine
**Linked Story:** [US-12: In-App Scrum Backlog, Sprint & Kanban Engine](USER_STORY.md#us-12-in-app-scrum-backlog--kanban-engine)

#### Scenario 1: Managing user stories and Kanban transitions
- **Given** the in-app Scrum management database,
- **When** a user story transitions from `In Progress` to `Review/Testing` or `Done`,
- **Then** the card's column updates in the database,
- **And** the terminal ASCII board and web Kanban board reflect the new status immediately.
