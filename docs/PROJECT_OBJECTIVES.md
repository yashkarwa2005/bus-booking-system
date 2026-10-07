# Project Objectives & Agile Syllabus Mapping
## Bus Booking System using Scrum Agile Methodology

---

## 1. Project Background & Context

This project is developed as an academic **Project-Based Learning (PBL)** submission for the **B.Tech 3rd-Year Agile Methodologies (AM)** curriculum by student **Archita**.

The project accomplishes two key goals:
1. **Domain Problem Solution:** Deliver an intuitive, high-reliability intercity Bus Booking System connecting passengers with bus operators, eliminating seat double-booking collisions, and enabling instant seat recycling.
2. **Pedagogical Demonstration:** Execute the software engineering lifecycle strictly following **Scrum Agile Methodology**, generating verifiable industry-standard artifacts and integrating Scrum project management directly into the delivered software.

---

## 2. Core Project Objectives

### Technical Objectives
- **Zero Double-Booking Guarantee:** Enforce atomic database transactions (`BEGIN IMMEDIATE`) so that no bus seat is ever double-booked under concurrent requests.
- **Dynamic Scheduling & Seat Inventory:** Allow bus operators to register fleet vehicles, map travel routes, and publish timetables with auto-generated seat layouts.
- **Full Lifecycle Management:** Support passenger search, seat selection, booking, viewing history, and cancellation with immediate seat vacancy recycling.
- **Portability & Zero Friction:** Engineer using pure Python standard libraries and SQLite to run flawlessly on any academic evaluation workstation without third-party dependencies.

### Agile Methodology Objectives
- **Scrum Framework Mastery:** Apply Scrum roles (Product Owner, Scrum Master, Developers), ceremonies (Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective), and artifacts (Product Backlog, Sprint Backlog, Shippable Increment).
- **Iterative & Incremental Delivery:** Partition system requirements into 5 weekly sprints, delivering demonstrable vertical slices each week.
- **Transparent Work Visualization:** Implement visual tracking using Markdown, terminal ASCII Kanban boards, and an interactive Web Kanban board.
- **Continuous Quality Assurance:** Couple every user story with testable Acceptance Criteria and automated unit tests satisfying the Definition of Done (DoD).

---

## 3. Direct Mapping to Agile Methodologies (AM) Syllabus

| Syllabus Concept | How Implemented in Project | Key Project Artifacts |
|---|---|---|
| **Agile Software Development** | Developed incrementally across 5 distinct sprints; responsive to feedback and iterative design. | [docs/SYSTEM_DESIGN.md](SYSTEM_DESIGN.md) |
| **Scrum Roles** | Clearly partitioned duties among Product Owner (Archita), Scrum Master, and Developers. | [scrum/SPRINT_PLAN.md](../scrum/SPRINT_PLAN.md) |
| **User Stories** | Formatted using standard Agile template (`As a... I want... So that...`) satisfying INVEST criteria. | [readme/USER_STORY.md](../readme/USER_STORY.md) |
| **Acceptance Criteria** | Formulated using Gherkin syntax (`Given - When - Then`) with verifiable edge cases. | [readme/ACCEPTANCE_CRITERIA.md](../readme/ACCEPTANCE_CRITERIA.md) |
| **Product Backlog** | Comprehensive list of ranked user stories with story points estimated via Planning Poker. | [scrum/PRODUCT_BACKLOG.md](../scrum/PRODUCT_BACKLOG.md) |
| **Requirement Prioritization** | Formalized using MoSCoW (🔴 Must Have, 🟠 Should Have, 🟢 Could Have, ⚪ Won't Have). | [scrum/REQUIREMENT_PRIORITIES.md](../scrum/REQUIREMENT_PRIORITIES.md) |
| **Sprint Planning** | Structured into 5 one-week sprints with defined goals, tasks, story point commitments, and velocity. | [scrum/SPRINT_PLAN.md](../scrum/SPRINT_PLAN.md) |
| **Sprint Execution** | Tracked via daily standup logs and in-app status transitions. | `src/sprint.py`, `src/action_item.py` |
| **Sprint Review** | Formal review records for each sprint evaluating completed increments with stakeholder feedback. | [scrum/SPRINT_REVIEW.md](../scrum/SPRINT_REVIEW.md) |
| **Sprint Retrospective** | Structured "What went well / What didn't / Improvements" sessions driving real process changes. | [scrum/SPRINT_RETROSPECTIVE.md](../scrum/SPRINT_RETROSPECTIVE.md) |
| **Action Items** | Weekly register tracking tasks with owners, due dates, priorities, and statuses. | [scrum/ACTION_ITEMS.md](../scrum/ACTION_ITEMS.md) |
| **Kanban Board** | 5-stage visual board (`Backlog -> Todo -> In Progress -> Review -> Done`) in Markdown, Terminal CLI & Web. | [scrum/KANBAN_BOARD.md](../scrum/KANBAN_BOARD.md), `src/kanban.py` |
| **Continuous Improvement** | Measured velocity stabilization and architectural refinements across sprints. | [scrum/SPRINT_RETROSPECTIVE.md](../scrum/SPRINT_RETROSPECTIVE.md) |
| **Automated Testing** | 16 automated unit test cases mapped directly to acceptance criteria with 100% pass rate. | [docs/TESTING.md](TESTING.md), `tests/test_bus_booking.py` |
| **Incremental Development** | Shippable increment produced at the end of every weekly iteration. | [scrum/SPRINT_PLAN.md](../scrum/SPRINT_PLAN.md) |
