# User Story Documentation
## Bus Booking System using Scrum Agile Methodology

---

## 1. What is a User Story?

In Agile and Scrum methodologies, a **User Story** is an informal, general explanation of a software feature written from the perspective of the end user or customer. Its primary purpose is to articulate how a software feature delivers measurable value to its consumers.

### Standard Agile Format
> **As a** `<type of user>`,  
> **I want** `<some goal / functionality>`,  
> **So that** `<some reason / benefit / value>`.

### The 3 C's of User Stories
1. **Card**: Written description of the story, serving as an invitation to conversation.
2. **Conversation**: Ongoing discussions between the Product Owner, Scrum Master, and Developers to clarify details.
3. **Confirmation**: Acceptance criteria that confirm the story has been implemented correctly and meets the Definition of Done (DoD).

### INVEST Criteria
All user stories in this project adhere strictly to the **INVEST** principle:
- **I**ndependent: Minimal overlap and dependency on other stories.
- **N**egotiable: Open to discussion and refinement during backlog grooming.
- **V**aluable: Delivers clear, tangible value to passengers, operators, or administrators.
- **E**stimable: Sized realistically using story points (Fibonacci scale: 1, 2, 3, 5, 8).
- **S**mall: Scoped to be completed within a single 1-week sprint iteration.
- **T**estable: Accompanied by verifiable Acceptance Criteria ([ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md)).

---

## 2. User Roles & Personas

| Role | Persona Name | Description & Context |
|---|---|---|
| **Passenger / Traveler** | Archita / Rahul | Needs a fast, transparent self-service portal to search intercity bus schedules, view available seat maps (window vs aisle), and book seats without double-booking risk. |
| **Bus Operator** | Suresh Joshi (Neeta Travels) | Fleet operator responsible for adding buses, configuring seating capacities, defining travel routes, and publishing departure timetables. |
| **System Administrator** | Vikram Patel | System administrator monitoring fleet utilization, auditing passenger bookings, and maintaining platform data integrity. |
| **Scrum Development Team** | Archita & Dev Team | Product Owner, Scrum Master, and Developers using built-in Scrum tooling to manage sprints, backlogs, and Kanban workflows. |

---

## 3. User Story Inventory & Backlog Mapping

The following table summarizes the complete set of User Stories mapped directly to the Product Backlog, Sprints, and MoSCoW priorities:

| Story ID | Story Title | Role | Priority | Story Points | Sprint | Status | Assignee |
|---|---|---|---|---|---|---|---|
| **US-01** | Passenger & Operator Registration | Passenger | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done | Archita |
| **US-02** | Credential Authentication & Role Session | All Roles | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done | Dev Team |
| **US-03** | Bus Fleet & Seating Capacity Management | Operator | 🔴 Must Have | 5 | Sprint 2 | 🟢 Done | Archita |
| **US-04** | Intercity Route & Distance Mapping | Operator | 🔴 Must Have | 5 | Sprint 2 | 🟢 Done | Dev Team |
| **US-05** | Bus Timetable & Dynamic Fare Scheduling | Operator | 🔴 Must Have | 3 | Sprint 2 | 🟢 Done | Dev Team |
| **US-06** | Search Buses by Corridor & Travel Date | Passenger | 🔴 Must Have | 5 | Sprint 3 | 🟢 Done | Dev Team |
| **US-07** | Real-Time Seat Layout & Vacancy Inspection | Passenger | 🔴 Must Have | 3 | Sprint 3 | 🟢 Done | Dev Team |
| **US-08** | Atomic Ticket Booking & Concurrency Lock | Passenger | 🔴 Must Have | 8 | Sprint 3 | 🟢 Done | Archita |
| **US-09** | Passenger Booking History & E-Ticket Details | Passenger | 🟠 Should Have | 3 | Sprint 4 | 🟢 Done | Dev Team |
| **US-10** | Ticket Cancellation & Immediate Seat Recovery | Passenger | 🔴 Must Have | 5 | Sprint 4 | 🟢 Done | Archita |
| **US-11** | Operator Passenger Manifest & Fleet Audit | Operator | 🟢 Could Have | 3 | Sprint 5 | 🟢 Done | Dev Team |
| **US-12** | In-App Scrum Backlog, Sprint & Kanban Engine | Scrum Team | 🔴 Must Have | 8 | Sprint 5 | 🟢 Done | Archita |

---

## 4. Detailed User Story Specifications

### US-01: Passenger & Operator Registration
- **Story ID:** `US-01`
- **User Role:** Passenger / User
- **User Story:**
  > **As a** new traveler or bus operator,  
  > **I want** to create a user account with username, password, email, and phone number,  
  > **So that** I can securely access bus reservation features.
- **Story Points:** 3 (Fibonacci Scale)
- **Target Sprint:** Sprint 1
- **MoSCoW Priority:** 🔴 Must Have
- **Acceptance Criteria Ref:** [AC-US01](ACCEPTANCE_CRITERIA.md#ac-us01-passenger--operator-registration)

---

### US-02: Credential Authentication & Role-Based Session
- **Story ID:** `US-02`
- **User Role:** All Roles (Passenger, Operator, Admin)
- **User Story:**
  > **As a** registered system user,  
  > **I want** to log in using my credentials,  
  > **So that** the platform authenticates my identity and loads my role-specific dashboard.
- **Story Points:** 3
- **Target Sprint:** Sprint 1
- **MoSCoW Priority:** 🔴 Must Have
- **Acceptance Criteria Ref:** [AC-US02](ACCEPTANCE_CRITERIA.md#ac-us02-credential-authentication--role-session)

---

### US-03: Bus Fleet & Seating Capacity Management
- **Story ID:** `US-03`
- **User Role:** Bus Operator
- **User Story:**
  > **As a** bus operator,  
  > **I want** to register new buses specifying bus number, bus type, and total seat capacity,  
  > **So that** my transportation inventory is cataloged for scheduling.
- **Story Points:** 5
- **Target Sprint:** Sprint 2
- **MoSCoW Priority:** 🔴 Must Have
- **Acceptance Criteria Ref:** [AC-US03](ACCEPTANCE_CRITERIA.md#ac-us03-bus-fleet-management)

---

### US-04: Intercity Route & Distance Mapping
- **Story ID:** `US-04`
- **User Role:** Bus Operator
- **User Story:**
  > **As a** bus operator,  
  > **I want** to define travel routes with origin city, destination city, distance, and duration,  
  > **So that** journeys can be mapped across legitimate transportation corridors.
- **Story Points:** 5
- **Target Sprint:** Sprint 2
- **MoSCoW Priority:** 🔴 Must Have
- **Acceptance Criteria Ref:** [AC-US04](ACCEPTANCE_CRITERIA.md#ac-us04-intercity-route-mapping)

---

### US-05: Bus Timetable & Dynamic Fare Scheduling
- **Story ID:** `US-05`
- **User Role:** Bus Operator
- **User Story:**
  > **As a** bus operator,  
  > **I want** to publish scheduled departures linking a bus, route, travel date, departure time, and ticket fare,  
  > **So that** passengers can view and book available trips.
- **Story Points:** 3
- **Target Sprint:** Sprint 2
- **MoSCoW Priority:** 🔴 Must Have
- **Acceptance Criteria Ref:** [AC-US05](ACCEPTANCE_CRITERIA.md#ac-us05-bus-timetable--fare-scheduling)

---

### US-06: Search Buses by Corridor & Travel Date
- **Story ID:** `US-06`
- **User Role:** Passenger
- **User Story:**
  > **As a** passenger,  
  > **I want** to search available buses by origin, destination, and travel date,  
  > **So that** I can compare available departures, bus types, and fares.
- **Story Points:** 5
- **Target Sprint:** Sprint 3
- **MoSCoW Priority:** 🔴 Must Have
- **Acceptance Criteria Ref:** [AC-US06](ACCEPTANCE_CRITERIA.md#ac-us06-search-buses-by-corridor)

---

### US-07: Real-Time Seat Layout & Vacancy Inspection
- **Story ID:** `US-07`
- **User Role:** Passenger
- **User Story:**
  > **As a** passenger,  
  > **I want** to inspect a visual seat matrix showing available vs booked seats,  
  > **So that** I can pick my preferred window or aisle seat before booking.
- **Story Points:** 3
- **Target Sprint:** Sprint 3
- **MoSCoW Priority:** 🔴 Must Have
- **Acceptance Criteria Ref:** [AC-US07](ACCEPTANCE_CRITERIA.md#ac-us07-seat-layout--vacancy-inspection)

---

### US-08: Atomic Ticket Booking & Concurrency Lock
- **Story ID:** `US-08`
- **User Role:** Passenger
- **User Story:**
  > **As a** passenger,  
  > **I want** to reserve my chosen seat atomically,  
  > **So that** it is locked immediately and no other passenger can double-book the same seat.
- **Story Points:** 8
- **Target Sprint:** Sprint 3
- **MoSCoW Priority:** 🔴 Must Have
- **Acceptance Criteria Ref:** [AC-US08](ACCEPTANCE_CRITERIA.md#ac-us08-atomic-ticket-booking--concurrency-lock)

---

### US-09: Passenger Booking History & E-Ticket Details
- **Story ID:** `US-09`
- **User Role:** Passenger
- **User Story:**
  > **As a** passenger,  
  > **I want** to view my active and past booking history with booking reference numbers,  
  > **So that** I can verify my travel details and show proof of reservation.
- **Story Points:** 3
- **Target Sprint:** Sprint 4
- **MoSCoW Priority:** 🟠 Should Have
- **Acceptance Criteria Ref:** [AC-US09](ACCEPTANCE_CRITERIA.md#ac-us09-passenger-booking-history)

---

### US-10: Ticket Cancellation & Immediate Seat Recovery
- **Story ID:** `US-10`
- **User Role:** Passenger
- **User Story:**
  > **As a** passenger,  
  > **I want** to cancel an existing confirmed reservation,  
  > **So that** my seat is immediately recycled into available inventory for other passengers.
- **Story Points:** 5
- **Target Sprint:** Sprint 4
- **MoSCoW Priority:** 🔴 Must Have
- **Acceptance Criteria Ref:** [AC-US10](ACCEPTANCE_CRITERIA.md#ac-us10-ticket-cancellation--seat-recovery)

---

### US-11: Operator Passenger Manifest & Fleet Audit
- **Story ID:** `US-11`
- **User Role:** Operator / Admin
- **User Story:**
  > **As an** operator or administrator,  
  > **I want** to inspect the global passenger manifest across all buses and routes,  
  > **So that** I can monitor vehicle occupancy and audit operational revenue.
- **Story Points:** 3
- **Target Sprint:** Sprint 5
- **MoSCoW Priority:** 🟢 Could Have
- **Acceptance Criteria Ref:** [AC-US11](ACCEPTANCE_CRITERIA.md#ac-us11-operator-passenger-manifest)

---

### US-12: In-App Scrum Backlog, Sprint & Kanban Engine
- **Story ID:** `US-12`
- **User Role:** Scrum Team Member / Evaluator
- **User Story:**
  > **As a** Scrum team member,  
  > **I want** an integrated Agile project management engine within the software,  
  > **So that** our team tracks user stories, sprint lifecycles, and Kanban progression in real time.
- **Story Points:** 8
- **Target Sprint:** Sprint 5
- **MoSCoW Priority:** 🔴 Must Have
- **Acceptance Criteria Ref:** [AC-US12](ACCEPTANCE_CRITERIA.md#ac-us12-in-app-scrum-backlog--kanban-engine)
