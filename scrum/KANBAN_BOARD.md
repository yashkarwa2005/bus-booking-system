# Kanban Board & Workflow
## Bus Booking System using Scrum Agile Methodology

---

## 1. Kanban Methodology Overview

**Kanban** is a visual workflow management method that emphasizes real-time capacity communication, limiting Work-in-Progress (WIP), and maximizing software delivery flow. In this project, the development lifecycle was visualized across five core stages:

```text
┌──────────────┐     ┌──────────────┐     ┌────────────────┐     ┌──────────────────┐     ┌──────────────┐
│   BACKLOG    │ ──> │     TODO     │ ──> │  IN PROGRESS   │ ──> │  REVIEW/TESTING  │ ──> │     DONE     │
└──────────────┘     └──────────────┘     └────────────────┘     └──────────────────┘     └──────────────┘
```

### Core Kanban Rules Applied:
1. **Visualize the Workflow:** All user stories and technical action items are represented as visual cards.
2. **Limit Work In Progress (WIP):** Maximum of 2 tasks per developer in `IN PROGRESS` to prevent multitasking bottlenecks.
3. **Manage Flow:** Daily scrums focus on advancing cards rightward towards `Done` before pulling new cards.
4. **Continuous Quality Gate:** Items cannot transition to `DONE` without passing automated unit test execution.

### Priority Badges:
- 🔴 **High Priority (Must Have)**
- 🟠 **Medium Priority (Should Have)**
- 🟢 **Low Priority (Could Have)**

---

## 2. Live Project Kanban Board (Sprint 5 Final State)

| 📋 BACKLOG | 🔵 TODO | 🟡 IN PROGRESS | 🟣 REVIEW / TESTING | 🟢 DONE |
|---|---|---|---|---|
| 🟢 `US-EXT-1` [3 pts]<br>Bus Amenities Filter (WiFi/Charging)<br>_Assignee: Unassigned_ | 🟢 `US-EXT-2` [2 pts]<br>SMS Notification Gateway Integration<br>_Assignee: Dev Team_ | 🟠 `AI-17` [2 pts]<br>Prepare System Design diagrams<br>_Assignee: Dev Team_ | 🔴 `AI-18` [3 pts]<br>Sprint Review & Viva rehearsal<br>_Assignee: Archita_ | 🔴 `US-01` [3 pts]<br>User Registration Module<br>_Assignee: Archita_ |
| 🟢 `US-EXT-3` [2 pts]<br>Luggage Tracking Add-on<br>_Assignee: Unassigned_ | | | | 🔴 `US-02` [3 pts]<br>Authentication & Session Auth<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-03` [5 pts]<br>Bus Fleet & Seat Capacity<br>_Assignee: Archita_ |
| | | | | 🔴 `US-04` [5 pts]<br>Intercity Route Mapping<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-05` [3 pts]<br>Timetable & Fare Scheduling<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-06` [5 pts]<br>Corridor Bus Search<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-07` [3 pts]<br>Seat Layout & Vacancy Map<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-08` [8 pts]<br>Atomic Seat Reservation Lock<br>_Assignee: Archita_ |
| | | | | 🟠 `US-09` [3 pts]<br>Passenger Booking History<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-10` [5 pts]<br>Cancel Ticket & Free Seat<br>_Assignee: Archita_ |
| | | | | 🟢 `US-11` [3 pts]<br>Operator Manifest & Fleet Audit<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-12` [8 pts]<br>In-App Scrum Kanban Engine<br>_Assignee: Archita_ |
| | | | | 🔴 `AI-16` [3 pts]<br>Automated Unit Tests (16/16)<br>_Assignee: Archita_ |

---

## 3. Terminal & Web Kanban Access

Evaluation machine instructions:
- **Terminal ASCII Board:** Run `python src/main.py --kanban` to view live board in console.
- **Interactive Web Board:** Run `python app.py` and open [http://localhost:5000/kanban](http://localhost:5000/kanban) to move cards dynamically across columns.
