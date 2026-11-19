# Next Step · Bay Area Graduate Job Dashboard

A Python dashboard by Joshua Milstead for 2026 graduates exploring MIS, business, and technology careers in the wider San Francisco Bay Area. Remote California roles are included when the location evidence supports them.

## Run the dashboard

Requires Python 3.12 or newer. The included real-data snapshot makes the app usable immediately; no API key is required.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Use the activation command for your operating system, then open the local URL printed by Streamlit.

## What it answers

- Which business and technology paths appear most often in the selected employer postings?
- Where are these opportunities located, and which skills do they mention?
- How often is pay disclosed, and where is there enough information to compare advertised pay?

Four interactive charts cover roles, locations, salary (or disclosure coverage when the sample is insufficient), and skills. Search and filters update all charts and a downloadable job table. Select a table row for the extracted experience evidence and the employer application link.

The default view prioritizes MIS/business paths, postings dated 2026, numeric experience minima of 0–2 years or entry/new-grad titles, and listings seen on the latest successful source check. Add Software & engineering to broaden the search. A title or numeric screen does not verify every eligibility requirement.

## Free deployment from GitHub

Recommended host: **Streamlit Community Cloud**, which runs the Python UI and shared backend in one app. No separate frontend service or paid API is needed.

1. Put these project files at the root of `Jmils25/Job-Dashboard-Bay-Area` on GitHub. Include `.github`, `.streamlit`, `config`, `data`, `jobradar`, `tests`, and the root files; exclude `.venv` and raw caches.
2. Sign in at <https://share.streamlit.io/> and connect your GitHub account.
3. Choose **Create app**, then select repository `Jmils25/Job-Dashboard-Bay-Area`, branch `main`, entrypoint `app.py`, and Python 3.12.
4. Deploy. Open the resulting `streamlit.app` link in a private window to verify public access.
5. In GitHub's **Actions** tab, enable workflows if prompted. Open **Refresh employer postings → Run workflow** for the first refresh.

The repository URL alone does not grant ChatGPT permission to push. GitHub authentication and the Streamlit account connection must be completed by the account owner when requested.

## Refresh the real data

```bash
python -m jobradar.ingest
```

`config/sources.json` lists the selected public Greenhouse and Lever employer boards. The collector fetches published jobs, screens geography and experience, extracts skill mentions, optionally reads structured compensation, and atomically replaces `data/jobs.json`.

The included GitHub Actions workflow requests a daily refresh at **14:23 UTC** (6:23 AM Pacific Standard Time / 7:23 AM Pacific Daylight Time). It also supports manual runs. It starts operating only after the repository is published and Actions is enabled; scheduled runs can be delayed and inactivity can disable schedules. The dashboard always shows the actual source-check timestamp and warns when the snapshot is over 48 hours old. A scheduled refresh is not an always-running live feed.

Failed sources retain their earlier postings as unverified. A job absent from a fully fetched board is marked no longer listed. An all-source failure preserves the last good snapshot. The site reads the committed dataset rather than querying employers for every visitor.

## Optional Python REST backend

The app uses `jobradar/service.py` directly. A separate read-only FastAPI interface is also included for a future custom frontend:

```bash
uvicorn jobradar.api:app --reload
```

Interactive API docs: <http://127.0.0.1:8000/docs>.

| Route | Purpose |
| --- | --- |
| `GET /health` | API health and snapshot timestamp |
| `GET /metadata` | Source coverage and refresh results |
| `GET /facets` | Available role, city, experience, and work-arrangement filters |
| `GET /jobs` | Search/filter with pagination |
| `GET /jobs/{job_id}` | One posting and its evidence |
| `GET /summary` | Aggregates for matching postings |
| `GET /export.csv` | Download matching results |

Example: `/jobs?q=SQL&year=2026&limit=20`. Use `year=0` for any year. Unknown experience and US remote with unverified California eligibility are excluded by default. Counts reflect distinct source postings after canonical-URL deduplication, not verified unique vacancies.

## Validation

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

Tests cover experience ambiguity, location collisions, remote eligibility, pay units, date handling, refresh failures, filters, CSV formula escaping, API validation, and dashboard load/empty states.

## Interpretation

This is a selected set of employer boards, not a representative census of all Bay Area hiring. The source list favors technology employers. Listing publication does not prove that a vacancy is still accepting applications. Requirements, dates, salary, and deadlines can be missing. Skills are text mentions, not necessarily requirements. Multiple locations can make city totals overlap. Full-time eligibility and application deadlines must be verified on the employer page. No applicants, resumes, or application submissions are collected.

See [DATA_SOURCES.md](DATA_SOURCES.md) for provenance, methodology, and data licensing. The chatbot is deferred to Part 2.
