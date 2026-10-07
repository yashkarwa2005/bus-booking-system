# Requirement Prioritization (MoSCoW Method)
## Bus Booking System using Scrum Agile Methodology

---

## 1. Overview of the MoSCoW Prioritization Framework

In Agile software engineering, requirements evolve rapidly based on user feedback, operational testing, and iteration constraints. To guarantee predictable, value-driven software delivery within fixed 1-week sprint iterations, the **MoSCoW** prioritization method is utilized:

- **🔴 MUST HAVE (M):** Non-negotiable requirements critical for the release. If any Must Have requirement is missing, the system cannot function as a viable bus booking platform.
- **🟠 SHOULD HAVE (S):** High-impact capabilities that significantly improve usability and efficiency, but can be worked around if time is strictly constrained.
- **🟢 COULD HAVE (C):** Desirable enhancements that offer convenience or administrative depth, delivered only when surplus sprint capacity exists.
- **⚪ WON'T HAVE (W):** Explicitly agreed out-of-scope capabilities for this release (e.g. online payment gateway integration, SMS gateway, real-time GPS vehicle tracking).

---

## 2. MoSCoW Category Breakdown

### 🔴 1. MUST HAVE (Critical Core — 35 Story Points)
Without these features, the Bus Booking System cannot perform basic passenger reservations or seat management:

| Story ID | Requirement Description | Story Points | Justification |
|---|---|---|---|
| **US-01** | Passenger & Operator Registration | 3 | Necessary to establish authenticated user accounts. |
| **US-02** | Credential Authentication & Role Session | 3 | Required for secure role separation (Passenger, Operator, Admin). |
| **US-03** | Bus Fleet & Capacity Management | 5 | Operators must register vehicles and physical seating layout. |
| **US-04** | Route Network & Distance Definition | 5 | Necessary to define travel corridors between source and destination. |
| **US-05** | Bus Timetable & Dynamic Fare Scheduling | 3 | Schedules must exist for passengers to have bookable departures. |
| **US-06** | Search Buses by Corridor & Travel Date | 5 | Fundamental passenger feature to find viable travel options. |
| **US-07** | Real-Time Seat Layout & Vacancy Inspection | 3 | Prerequisite for passenger seat choice (window vs aisle). |
| **US-08** | Atomic Seat Reservation & Concurrency Lock | 8 | Core transactional requirement: strictly prevents double-booking race conditions. |
| **US-10** | Ticket Cancellation & Immediate Seat Recovery | 5 | Essential for recycling bus inventory upon booking changes. |

---

### 🟠 2. SHOULD HAVE (Important Enhancements — 6 Story Points)
These features substantially improve passenger convenience, workflow feedback, and record-keeping:

| Story ID | Requirement Description | Story Points | Justification |
|---|---|---|---|
| **US-09** | Passenger Booking History & E-Ticket Details | 3 | Allows passengers to retrieve confirmation receipts and travel itineraries. |
| **US-12** | In-App Scrum Backlog, Sprint & Kanban Management Engine | 3 | Academic requirement to demonstrate active Scrum workflow within the running application. |

---

### 🟢 3. COULD HAVE (Desirable Features — 8 Story Points)
These items add convenience and administrative visibility without blocking the core booking workflow:

| Story ID | Requirement Description | Story Points | Justification |
|---|---|---|---|
| **US-11** | Operator Passenger Manifest & Fleet Audit | 3 | Centralized reporting for bus operators to monitor vehicle occupancy. |
| **US-12 (Ext)** | Terminal ANSI Color Badges & Web Live Kanban Dashboard | 5 | Enhances terminal and browser evaluation ergonomics for evaluators. |

---

### ⚪ 4. WON'T HAVE (Deferred for Future Roadmap)
- **Third-Party Payment Gateways (Stripe/Razorpay):** Offline / cash-at-boarding simulated for academic focus.
- **Automated SMS Gateway:** Simulating e-ticket confirmation in-app instead of paid carrier SMS.
- **Real-Time GPS Vehicle Telematics:** Requires IoT onboard hardware, out of scope for software PBL.

---

## 3. Priority Summary Table

| Category | Story Count | Total Story Points | Percentage of Effort |
|---|---|---|---|
| 🔴 **Must Have** | 9 Stories | 35 Points | 71.4% |
| 🟠 **Should Have** | 2 Stories | 6 Points | 12.2% |
| 🟢 **Could Have** | 2 Stories | 8 Points | 16.4% |
| **Total** | **13 Items** | **49 Points** | **100.0%** |
