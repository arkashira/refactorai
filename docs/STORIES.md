# STORIES.md

## RefactorAI – User Story Backlog

> **Goal:** Deliver a lightweight, data‑driven dashboard that visualises the impact of refactoring actions on code‑quality metrics, enabling teams to track progress, justify refactoring investments, and surface actionable insights.

---

## Epics & Stories

| Epic | Story | Acceptance Criteria |
|------|-------|---------------------|
| **E1. Core Refactoring Action Management** | **S1.** *As a developer, I want to add a refactoring action to the system, so that I can record the effort and impact of my changes.* | • `add_action` accepts `org`, `repo`, `effort`, `impact`, and `date`. <br>• Action is persisted in an in‑memory list (or DB stub). <br>• Duplicate actions for the same `org/repo/date` are rejected with a clear error. |
| | **S2.** *As a developer, I want to view all refactoring actions for a given repository, so that I can audit past work.* | • `list_actions(repo)` returns a list sorted by date descending. <br>• Each item includes `org`, `effort`, `impact`, `date`. |
| | **S3.** *As a developer, I want to delete a refactoring action, so that I can correct mistakes.* | • `delete_action(action_id)` removes the action. <br>• Confirmation prompt (CLI) or safe‑delete flag. |
| **E2. Weekly Metrics Aggregation** | **S4.** *As a product owner, I want to retrieve weekly metrics, so that I can see trends over time.* | • `get_weekly_metrics()` returns a list of weeks with: <br> • `week_start`, `total_actions`, `avg_effort`, `avg_impact`, `cumulative_impact`. <br>• Weeks are ISO‑8601 week numbers. |
| | **S5.** *As a data analyst, I want to filter weekly metrics by organization, so that I can compare teams.* | • `get_weekly_metrics(org='org1')` returns metrics only for that org. |
| **E3. CSV Export** | **S6.** *As a stakeholder, I want to export weekly metrics to CSV, so that I can share them in reports.* | • `export_csv(metrics)` returns a CSV string with header row. <br>• CSV is UTF‑8 encoded and includes all fields from metrics. |
| **E4. Authentication Layer** | **S7.** *As a user, I want to authenticate with an API key, so that only authorized users can access data.* | • `authenticate(api_key)` stores key in memory. <br>• All subsequent calls check key; unauthenticated calls raise `PermissionError`. |
| | **S8.** *As an admin, I want to rotate API keys, so that I can revoke compromised keys.* | • `rotate_key(old_key, new_key)` replaces key after validation. |
| **E5. Dashboard UI (MVP)** | **S9.** *As a product manager, I want a simple web dashboard that displays weekly metrics in a bar chart, so that I can quickly spot trends.* | • Dashboard loads metrics via `/api/weekly_metrics`. <br>• Bar chart shows `week_start` on X and `cumulative_impact` on Y. <br>• Refreshes every 5 minutes. |
| | **S10.** *As a developer, I want a table view of refactoring actions, so that I can drill down into details.* | • Table lists `org`, `repo`, `effort`, `impact`, `date`. <br>• Supports pagination (10 rows per page). |
| **E6. Validation & Testing** | **S11.** *As a QA engineer, I want unit tests for all public methods, so that regressions are caught early.* | • ≥80% code coverage. <br>• Tests cover edge cases (e.g., no actions, future dates). |
| | **S12.** *As a DevOps engineer, I want a CI pipeline that runs tests on every push, so that code quality is maintained.* | • GitHub Actions workflow runs tests on Python 3.10+. <br>• Fails on coverage <80%. |
| **E7. Documentation & Examples** | **S13.** *As a new user, I want a README with usage examples, so that I can get started quickly.* | • README includes code snippets for adding actions, retrieving metrics, exporting CSV, and authenticating. |
| | **S14.** *As a maintainer, I want inline docstrings for all public APIs, so that IDEs can provide help.* | • Each method has a concise docstring following Google style. |
| **E8. Future Enhancements (Optional)** | **S15.** *As a product owner, I want to add a “compare repos” feature, so that I can benchmark refactoring impact across teams.* | • `/api/compare_repos?repo1=&repo2=` returns side‑by‑side metrics. <br>• Feature flagged behind a config toggle. |

---

## MVP Release Order

1. **S1** – Core action addition (E1)
2. **S4** – Weekly metrics aggregation (E2)
3. **S6** – CSV export (E3)
4. **S7** – Authentication (E4)
5. **S9** – Dashboard bar chart (E5)
6. **S11** – Unit tests (E6)
7. **S13** – README examples (E7)

---

## Notes

- All dates are timezone‑agnostic; store as UTC `datetime` objects.
- Persisted data can initially be an in‑memory list; later replace with a lightweight DB (SQLite) if needed.
- API key can be a simple string; consider hashing for production.
- Use `pandas` for CSV generation and metric aggregation to keep implementation concise.

---
