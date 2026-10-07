# Action Items Register
## Bus Booking System using Scrum Agile Methodology

---

## 1. Action Items Management in Scrum

In Scrum, **Action Items** are concrete, measurable tasks identified during **Sprint Planning**, **Daily Scrum**, or **Sprint Retrospectives** to drive forward delivery and eliminate technical impediments.

### Status Indicators:
- 🔵 **To Do:** Item is queued for implementation in the sprint.
- 🟡 **In Progress:** Work is currently actively underway.
- 🟣 **Review:** Feature is coded and undergoing automated unit testing or peer review.
- 🟢 **Done:** Item is fully verified against the Definition of Done.
- 🔴 **Blocked:** Item is stalled due to an external roadblock.

---

## 2. Weekly Action Items Register

| ID | Action Item | Sprint | Owner | Priority | Due Date | Status |
|---|---|---|---|---|---|---|
| **AI-01** | Initialize repository structure, `.gitignore`, and licensing | Sprint 1 | Archita | 🔴 High | Week 1 - Day 2 | 🟢 Done |
| **AI-02** | Design normalized SQLite schema with foreign key cascades | Sprint 1 | Dev Team | 🔴 High | Week 1 - Day 4 | 🟢 Done |
| **AI-03** | Implement SHA-256 password salting and hashing module | Sprint 1 | Archita | 🔴 High | Week 1 - Day 5 | 🟢 Done |
| **AI-04** | Draft INVEST User Stories and Gherkin Acceptance Criteria | Sprint 1 | Archita | 🟠 Medium | Week 1 - Day 6 | 🟢 Done |
| **AI-05** | Build Bus Fleet and Seating Layout models | Sprint 2 | Dev Team | 🔴 High | Week 2 - Day 3 | 🟢 Done |
| **AI-06** | Construct Route directory and schedule publishing service | Sprint 2 | Archita | 🔴 High | Week 2 - Day 4 | 🟢 Done |
| **AI-07** | Populate realistic bus corridors (Pune-Mumbai, Mumbai-Goa) | Sprint 2 | Dev Team | 🟢 Low | Week 2 - Day 6 | 🟢 Done |
| **AI-08** | Build origin-destination bus schedule search query | Sprint 3 | Dev Team | 🔴 High | Week 3 - Day 3 | 🟢 Done |
| **AI-09** | Implement dynamic seat layout matrix and vacancy counter | Sprint 3 | Dev Team | 🔴 High | Week 3 - Day 4 | 🟢 Done |
| **AI-10** | Engineer atomic seat booking transaction with concurrency lock | Sprint 3 | Archita | 🔴 High | Week 3 - Day 5 | 🟢 Done |
| **AI-11** | Build booking cancellation with automatic seat vacancy recycling | Sprint 4 | Archita | 🔴 High | Week 4 - Day 3 | 🟢 Done |
| **AI-12** | Construct passenger booking history and e-ticket summary | Sprint 4 | Dev Team | 🟠 Medium | Week 4 - Day 5 | 🟢 Done |
| **AI-13** | Develop operator passenger manifest and occupancy inspection | Sprint 5 | Dev Team | 🟠 Medium | Week 5 - Day 2 | 🟢 Done |
| **AI-14** | Implement SQLite-backed in-app Scrum Backlog & Sprint service | Sprint 5 | Archita | 🔴 High | Week 5 - Day 3 | 🟢 Done |
| **AI-15** | Construct interactive terminal ASCII Kanban board renderer | Sprint 5 | Archita | 🔴 High | Week 5 - Day 4 | 🟢 Done |
| **AI-16** | Write 16 automated unit and integration tests with 100% pass rate | Sprint 5 | Archita | 🔴 High | Week 5 - Day 5 | 🟢 Done |
| **AI-17** | Prepare comprehensive System Design diagrams & ERD | Sprint 5 | Dev Team | 🟠 Medium | Week 5 - Day 6 | 🟢 Done |
| **AI-18** | Synchronize GitHub repository, Issues, and final Viva release | Sprint 5 | Archita | 🔴 High | Week 5 - Day 7 | 🟢 Done |

---

## 3. Retrospective Continuous Improvement Action Items

| Source Ceremony | Identified Issue | Agreed Improvement Action | Owner | Outcome |
|---|---|---|---|---|
| **Sprint 1 Retrospective** | Manual database testing caused test delays | Introduce an isolated temporary SQLite database fixture | Archita | Implemented in Sprint 2; reduced test suite cycle to 1.1s. |
| **Sprint 2 Retrospective** | Hardcoded route distances created inconsistencies | Enforce foreign key constraints (`PRAGMA foreign_keys = ON;`) | Dev Team | Guaranteed relational referential integrity across schedules and seats. |
| **Sprint 3 Retrospective** | High risk of double-booking under concurrency | Wrap booking in `BEGIN IMMEDIATE` transaction lock | Archita | Concurrency collisions eliminated 100%. |
| **Sprint 4 Retrospective** | Need for rapid evaluator demonstration | Create `--demo` automated walkthrough | Archita | Enabled complete viva walkthrough in <30s. |
