# Automated Testing & Quality Assurance Report
## Bus Booking System using Scrum Agile Methodology

---

## 1. Testing Strategy & Philosophy

In Scrum Agile software engineering, quality is built in at every step rather than tested at the end. Every User Story has verifiable **Acceptance Criteria**, which serve as the formal specification for automated unit and integration tests.

### Key Testing Principles:
- **Zero Third-Party Hurdles:** Test suite uses Python's built-in `unittest` runner, requiring no external packages.
- **Fixture Isolation:** Each test method initializes a temporary SQLite database file using `tempfile.NamedTemporaryFile` in `setUp()` and unlinks it in `tearDown()`, ensuring total test independence.
- **Concurrency & Race Condition Coverage:** Specific test cases simulate concurrent double-booking conflicts to verify transactional locking.
- **100% Pass Criterion:** The Definition of Done (DoD) requires 100% test pass rate prior to release increment acceptance.

---

## 2. Requirements Traceability Matrix (RTM)

The following matrix maps automated test cases directly to User Stories and Acceptance Criteria:

| Test Case ID | Test Method Name | Linked Story | Story Title | Expected Outcome | Execution Result |
|---|---|---|---|---|---|
| **TC-01** | `test_tc01_user_registration_success` | `US-01` | Passenger Registration | New user created with salted SHA-256 hash | 🟢 PASSED |
| **TC-02** | `test_tc02_duplicate_user_registration_rejection` | `US-01` | Registration Validation | Duplicate username/email raises `ValueError` | 🟢 PASSED |
| **TC-03** | `test_tc03_user_login_success` | `US-02` | Credential Authentication | Valid credentials return user session dict | 🟢 PASSED |
| **TC-04** | `test_tc04_user_login_invalid_credentials_rejected` | `US-02` | Authentication Rejection | Wrong password or invalid user rejected | 🟢 PASSED |
| **TC-05** | `test_tc05_add_bus_success` | `US-03` | Bus Fleet Management | New bus registered with seating capacity | 🟢 PASSED |
| **TC-06** | `test_tc06_add_route_and_validation` | `US-04` | Intercity Route Mapping | Valid corridor stored; identical source/dest rejected | 🟢 PASSED |
| **TC-07** | `test_tc07_add_schedule_and_auto_seat_generation` | `US-05` | Schedule Publication | Schedule created and 24 seat records auto-generated | 🟢 PASSED |
| **TC-08** | `test_tc08_search_buses_by_corridor` | `US-06` | Corridor Bus Search | Origin-destination search returns available buses | 🟢 PASSED |
| **TC-09** | `test_tc09_inspect_seat_map_availability` | `US-07` | Seat Map Inspection | Returns seat layout distinguishing booked vs open | 🟢 PASSED |
| **TC-10** | `test_tc10_atomic_booking_success` | `US-08` | Atomic Ticket Booking | Locks seat, returns unique ref, sets status Confirmed | 🟢 PASSED |
| **TC-11** | `test_tc11_double_booking_concurrency_rejection` | `US-08` | Double-Booking Guard | Blocks duplicate booking of same seat atomically | 🟢 PASSED |
| **TC-12** | `test_tc12_cancellation_and_automatic_seat_recycling` | `US-10` | Ticket Cancellation | Marks status Cancelled and recycles seat to open | 🟢 PASSED |
| **TC-13** | `test_tc13_passenger_booking_history` | `US-09` | Passenger Itinerary History | Returns chronological booking records for user | 🟢 PASSED |
| **TC-14** | `test_tc14_global_manifest_and_stats` | `US-11` | Operator Manifest & Audit | Returns all bookings and aggregate statistics | 🟢 PASSED |
| **TC-15** | `test_tc15_scrum_user_story_lifecycle` | `US-12` | Scrum User Story Engine | Creates story and updates status across Kanban | 🟢 PASSED |
| **TC-16** | `test_tc16_sprint_metrics_and_kanban_rendering` | `US-12` | In-App Kanban Board | Calculates sprint velocity and renders ASCII board | 🟢 PASSED |

---

## 3. Actual Test Execution Log

```text
test_tc01_user_registration_success (tests.test_bus_booking.TestBusBookingSystem.test_tc01_user_registration_success)
TC-01: Verify successful passenger registration with valid credentials. ... ok
test_tc02_duplicate_user_registration_rejection (tests.test_bus_booking.TestBusBookingSystem.test_tc02_duplicate_user_registration_rejection)
TC-02: Verify duplicate username or email is rejected. ... ok
test_tc03_user_login_success (tests.test_bus_booking.TestBusBookingSystem.test_tc03_user_login_success)
TC-03: Verify successful authentication with valid credentials. ... ok
test_tc04_user_login_invalid_credentials_rejected (tests.test_bus_booking.TestBusBookingSystem.test_tc04_user_login_invalid_credentials_rejected)
TC-04: Verify rejection of invalid username or incorrect password. ... ok
test_tc05_add_bus_success (tests.test_bus_booking.TestBusBookingSystem.test_tc05_add_bus_success)
TC-05: Verify operator can register a new bus with seat capacity. ... ok
test_tc06_add_route_and_validation (tests.test_bus_booking.TestBusBookingSystem.test_tc06_add_route_and_validation)
TC-06: Verify route creation and rejection of identical source and destination. ... ok
test_tc07_add_schedule_and_auto_seat_generation (tests.test_bus_booking.TestBusBookingSystem.test_tc07_add_schedule_and_auto_seat_generation)
TC-07: Verify schedule generation auto-populates seat inventory. ... ok
test_tc08_search_buses_by_corridor (tests.test_bus_booking.TestBusBookingSystem.test_tc08_search_buses_by_corridor)
TC-08: Verify origin-destination search returns available schedules. ... ok
test_tc09_inspect_seat_map_availability (tests.test_bus_booking.TestBusBookingSystem.test_tc09_inspect_seat_map_availability)
TC-09: Verify seat map inspection correctly distinguishes booked and open seats. ... ok
test_tc10_atomic_booking_success (tests.test_bus_booking.TestBusBookingSystem.test_tc10_atomic_booking_success)
TC-10: Verify atomic ticket reservation locks seat and returns booking ref. ... ok
test_tc11_double_booking_concurrency_rejection (tests.test_bus_booking.TestBusBookingSystem.test_tc11_double_booking_concurrency_rejection)
TC-11: Verify defensive concurrency guard blocks duplicate booking of same seat. ... ok
test_tc12_cancellation_and_automatic_seat_recycling (tests.test_bus_booking.TestBusBookingSystem.test_tc12_cancellation_and_automatic_seat_recycling)
TC-12: Verify ticket cancellation marks status Cancelled and recycles seat to is_booked=0. ... ok
test_tc13_passenger_booking_history (tests.test_bus_booking.TestBusBookingSystem.test_tc13_passenger_booking_history)
TC-13: Verify passenger can retrieve their chronological booking history. ... ok
test_tc14_global_manifest_and_stats (tests.test_bus_booking.TestBusBookingSystem.test_tc14_global_manifest_and_stats)
TC-14: Verify administrative oversight returns manifest and summary stats. ... ok
test_tc15_scrum_user_story_lifecycle (tests.test_bus_booking.TestBusBookingSystem.test_tc15_scrum_user_story_lifecycle)
TC-15: Verify creation, validation, and Kanban status transition of user stories. ... ok
test_tc16_sprint_metrics_and_kanban_rendering (tests.test_bus_booking.TestBusBookingSystem.test_tc16_sprint_metrics_and_kanban_rendering)
TC-16: Verify sprint metrics and ASCII Kanban board generation. ... ok

----------------------------------------------------------------------
Ran 16 tests in 1.103s

OK
```

---

## 4. How to Execute Tests

To re-run the automated test suite locally:

```bash
# From the project root:
python -m unittest tests/test_bus_booking.py -v
```
