# Sprint Retrospective Reports
## Bus Booking System using Scrum Agile Methodology

---

## 1. Purpose of the Sprint Retrospective

The **Sprint Retrospective** is a regular ceremony occurring at the end of each sprint where the Scrum Team reflects on people, processes, tools, and relationships. Its goal is continuous process improvement by identifying what went well, what challenges arose, and actionable commitments for the next sprint.

---

## 2. Sprint 1 Retrospective

### What Went Well 👍
- Solid architectural foundation established with SQLite foreign keys and salted SHA-256 password security.
- Rapid consensus reached on INVEST-compliant user stories and Gherkin acceptance criteria.

### Challenges Encountered ⚠️
- Running tests directly against the default database file occasionally left residual test records.

### Action Items for Next Sprint 🎯
- **Adopt Temporary Test Fixtures:** Use `tempfile.NamedTemporaryFile` in unit tests for complete isolation (`AI-02`).

---

## 3. Sprint 2 Retrospective

### What Went Well 👍
- Clean relational design separating buses, routes, schedules, and dynamic seat records.
- Automatic creation of seat records (`1A` to `6D`) during schedule creation proved highly efficient.

### Challenges Encountered ⚠️
- Bus operators initially lacked clear boundaries for bus types and capacity limits.

### Action Items for Next Sprint 🎯
- Enforce strict CHECK constraints in SQLite for `bus_type` and seat range validations.

---

## 4. Sprint 3 Retrospective

### What Went Well 👍
- Concurrency lock using `BEGIN IMMEDIATE` and atomic transaction updates completely eliminated double-booking vulnerabilities.
- Passenger origin-destination search delivered instantaneous query response times.

### Challenges Encountered ⚠️
- Sizing the booking user story (`US-08`) was challenging due to concurrency race conditions; points were revised from 5 to 8 during grooming.

### Action Items for Next Sprint 🎯
- Add explicit unit tests simulating concurrent double-booking conflicts to permanently defend against regression (`TC-11`).

---

## 5. Sprint 4 Retrospective

### What Went Well 👍
- Cancellation workflow immediately unlocked the seat in the database (`is_booked = 0`), recycling capacity seamlessly.
- Chronological passenger booking history was easy to navigate and review.

### Challenges Encountered ⚠️
- Terminal console outputs were becoming dense with table data.

### Action Items for Next Sprint 🎯
- Build both an ANSI-colored console interface and a dedicated web dashboard using Python standard library `http.server`.

---

## 6. Sprint 5 Retrospective

### What Went Well 👍
- In-app terminal Kanban board and responsive web dashboard provided outstanding visual project transparency.
- 16/16 automated unit tests executed cleanly in ~1.1 seconds.
- `--demo` mode allows evaluators to witness the entire booking and Scrum workflow in under 30 seconds.

### Key Retrospective Takeaways 💡
- Disciplined Scrum cadence provided predictable velocity throughout all 5 weeks.
- Dual-track architecture (core domain + embedded Scrum engine) was a massive success for academic evaluation.
