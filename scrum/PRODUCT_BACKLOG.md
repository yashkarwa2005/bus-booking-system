# Product Backlog
## Bus Booking System using Scrum Agile Methodology

---

## 1. Product Vision & Backlog Strategy

### Vision Statement
> *"To engineer a resilient, transparent intercity bus booking platform that eliminates seat double-booking collisions, provides real-time seat availability maps, and streamlines passenger ticket lifecycle management, while practicing authentic Scrum Agile software engineering."*

### Product Backlog Overview
The **Product Backlog** is an emergent, ordered list of what is needed to improve the product. It is the single authoritative source of work undertaken by the Scrum Team, prioritized by the **Product Owner (Archita)**.

Items are ranked according to:
1. **Business Value & Core Viability** (MoSCoW priority).
2. **Technical Feasibility & Architectural Dependencies** (Database schema and authentication prior to booking logic).
3. **Risk Mitigation** (Addressing double-booking race conditions early in Sprint 3).

---

## 2. Product Epics & Architecture Themes

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       BUS BOOKING SYSTEM - PRODUCT EPICS                    │
└─────────────────────────────────────────────────────────────────────────────┘
     │
     ├── EPIC 1: Security & Identity Management (US-01, US-02)
     ├── EPIC 2: Fleet, Route & Timetable Operations (US-03, US-04, US-05)
     ├── EPIC 3: Discovery, Seat Layout & Atomic Lock Engine (US-06, US-07, US-08)
     ├── EPIC 4: Ticket Lifecycle & Automatic Seat Recovery (US-09, US-10)
     └── EPIC 5: Fleet Oversight & In-App Scrum Governance (US-11, US-12)
```

---

## 3. Prioritized Product Backlog Inventory

| Rank | Story ID | Title & Epic | Role | Priority | Story Points | Sprint Target | Status |
|---|---|---|---|---|---|---|---|
| **01** | `US-01` | Passenger & Operator Registration (Epic 1) | Passenger | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done |
| **02** | `US-02` | Credential Authentication & Role Session (Epic 1) | All Users | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done |
| **03** | `US-03` | Bus Fleet & Seating Specifications Management (Epic 2) | Operator | 🔴 Must Have | 5 | Sprint 2 | 🟢 Done |
| **04** | `US-04` | Route Network & Distance Definition (Epic 2) | Operator | 🔴 Must Have | 5 | Sprint 2 | 🟢 Done |
| **05** | `US-05` | Bus Timetable & Dynamic Fare Scheduling (Epic 2) | Operator | 🔴 Must Have | 3 | Sprint 2 | 🟢 Done |
| **06** | `US-06` | Search Buses by Corridor & Travel Date (Epic 3) | Passenger | 🔴 Must Have | 5 | Sprint 3 | 🟢 Done |
| **07** | `US-07` | Dynamic Seat Map & Availability Inspection (Epic 3) | Passenger | 🔴 Must Have | 3 | Sprint 3 | 🟢 Done |
| **08** | `US-08` | Atomic Seat Reservation & Concurrency Lock (Epic 3) | Passenger | 🔴 Must Have | 8 | Sprint 3 | 🟢 Done |
| **09** | `US-09` | Passenger Booking History & E-Ticket Details (Epic 4) | Passenger | 🟠 Should Have | 3 | Sprint 4 | 🟢 Done |
| **10** | `US-10` | Ticket Cancellation & Immediate Seat Recovery (Epic 4) | Passenger | 🔴 Must Have | 5 | Sprint 4 | 🟢 Done |
| **11** | `US-11` | Operator Passenger Manifest & Fleet Audit (Epic 5) | Operator | 🟢 Could Have | 3 | Sprint 5 | 🟢 Done |
| **12** | `US-12` | In-App Scrum Backlog, Sprint & Kanban Engine (Epic 5) | Scrum Team | 🔴 Must Have | 8 | Sprint 5 | 🟢 Done |

**Total Estimated Backlog Effort:** 49 Story Points  
**Estimation Scale:** Modified Fibonacci Sequence (1, 2, 3, 5, 8, 13) estimated via Planning Poker.

---

## 4. Backlog Refinement (Grooming) Ceremonies

Backlog grooming occurred mid-sprint to keep items ready for future sprint planning:
1. **Slicing Booking Work:** The initial monolithic *"Seat Reservation"* requirement was broken into three discrete, testable stories: `US-07 (Seat Map Display)`, `US-08 (Atomic Concurrency Lock)`, and `US-10 (Cancellation & Recycling)`.
2. **Defensive Concurrency Review:** During grooming for Sprint 3, the estimate for `US-08` was increased from 5 to 8 story points to account for multi-user race condition protection using SQLite atomic transactions.
3. **Definition of Ready (DoR):** All stories entering sprint planning contained Gherkin-formatted acceptance criteria, clear user persona justifications, and Fibonacci point estimates.

---

## 5. Artifact Links
- User Stories Detail: [readme/USER_STORY.md](../readme/USER_STORY.md)
- Acceptance Criteria Detail: [readme/ACCEPTANCE_CRITERIA.md](../readme/ACCEPTANCE_CRITERIA.md)
