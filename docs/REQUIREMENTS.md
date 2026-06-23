# REQUIREMENTS.md

## Project Overview
**RefactorAI** is a lightweight analytics dashboard that aggregates refactoring actions across multiple repositories, computes weekly code‑quality metrics, and presents the results in a user‑friendly format. The system is designed to be embedded in existing CI/CD pipelines or used as a standalone service for continuous improvement tracking.

---

## Functional Requirements

| ID | Description | Trigger | Output |
|----|-------------|---------|--------|
| **FR‑1** | **Create RefactorAI instance** | `refactor_ai = RefactorAI()` | Instance initialized with empty state and default configuration. |
| **FR‑2** | **Authenticate API key** | `refactor_ai.authenticate('api_key')` | Stores a validated API key; subsequent calls require authentication. |
| **FR‑3** | **Add a refactoring action** | `refactor_ai.add_action(action)` where `action` is a `RefactoringAction` object | Action appended to internal store; action includes: organization, repository, quality impact score, time spent, timestamp. |
| **FR‑4** | **Retrieve weekly metrics** | `metrics = refactor_ai.get_weekly_metrics()` | Returns a list of `WeeklyMetric` objects, each containing: week start/end, number of actions, average quality impact, total time spent, repository breakdown. |
| **FR‑5** | **Export metrics to CSV** | `csv_data = refactor_ai.export_csv(metrics)` | Returns a CSV string (or writes to file) with columns: `week_start, week_end, org, repo, actions, avg_quality, total_time`. |
| **FR‑6** | **Persist state** | Optional: `refactor_ai.save_state(filepath)` | Serializes current actions to a JSON/SQLite file. |
| **FR‑7** | **Load persisted state** | Optional: `refactor_ai.load_state(filepath)` | Restores actions from a previously saved file. |
| **FR‑8** | **Validate input data** | All public methods | Raise descriptive `ValueError` for missing or malformed fields. |
| **FR‑9** | **Handle authentication failures** | Any method requiring auth | Raise `AuthenticationError` if API key is missing or invalid. |
| **FR‑10** | **Support timezone‑aware timestamps** | `add_action` | Accepts `datetime` objects with timezone info; normalizes to UTC. |

---

## Non‑Functional Requirements

| ID | Category | Requirement |
|----|----------|-------------|
| **NFR‑1** | **Performance** | `get_weekly_metrics()` must return results for up to 10,000 actions in < 200 ms on a standard 4‑core machine. |
| **NFR‑2** | **Scalability** | The system should handle incremental growth to 100,000 actions without significant refactoring. |
| **NFR‑3** | **Security** | API key must be stored in memory only; never written to disk or logged. |
| **NFR‑4** | **Reliability** | All public methods must be idempotent where appropriate (e.g., adding the same action twice should not duplicate). |
| **NFR‑5** | **Usability** | Clear, concise error messages; method signatures follow PEP 8. |
| **NFR‑6** | **Extensibility** | Design allows adding new metrics (e.g., code churn) without breaking existing API. |
| **NFR‑7** | **Data Integrity** | All persisted data must be validated against a JSON schema before loading. |
| **NFR‑8** | **Compliance** | No personal data is stored; all timestamps are UTC. |

---

## Constraints

1. **Python Version** – Must run on Python 3.11+.
2. **Dependencies** – Only standard library and `pandas` (for CSV export) are allowed.
3. **Storage** – In‑memory data structures; optional persistence via JSON/SQLite.
4. **Authentication** – Simple API key string; no external auth services.
5. **Time Granularity** – Weekly metrics are based on ISO week numbers (Monday‑Sunday).

---

## Assumptions

1. **Input Validity** – Caller provides well‑formed `RefactoringAction` objects; otherwise, validation errors are raised.
2. **Time Zone** – All timestamps provided are timezone‑aware; if naive, assume UTC.
3. **Data Volume** – Typical usage involves < 10,000 actions per week; larger volumes are edge cases.
4. **Environment** – The dashboard runs in a trusted environment; no need for network isolation.

---

## Deliverables

1. `refactor_ai.py` – Core implementation with classes `RefactorAI`, `RefactoringAction`, `WeeklyMetric`.
2. `tests/` – Unit tests covering all functional and non‑functional requirements.
3. `requirements.txt` – Only `pandas` listed.
4. `README.md` – Updated with usage examples and API reference.

---

## Acceptance Criteria

- All functional requirements pass automated tests.
- Performance benchmark meets NFR‑1 on a 4‑core machine.
- Security review confirms API key is never persisted or logged.
- Documentation includes clear error handling examples.

---
