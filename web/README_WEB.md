# ProfOcto Web UI

A React 18 frontend with a FastAPI backend for running research gap debates in the browser.

---

## Prerequisites

- **Node.js 18+** — [nodejs.org](https://nodejs.org)
- **Python 3.10+** with virtual environment already set up (see [main setup guide](../docs/guides/02_SETUP.md))
- **Gemini API key** configured in `.env`

---

## Quick Start

You need two terminals running simultaneously.

### Terminal 1: FastAPI Backend

```bash
# From the project root
# Activate the virtual environment first:
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux

# Start the backend server
uvicorn web.server:app --reload --port 8000
```

### Terminal 2: React Frontend

```bash
cd web
npm install    # first time only
npm run dev
```

Open http://127.0.0.1:3000/ in your browser.

---

## Production Build

```bash
cd web
npm run build
```

After building, FastAPI serves the React frontend from the `web/dist/` directory. You only need to run the backend:

```bash
uvicorn web.server:app --port 8000
```

Then open http://localhost:8000.

---

## API Endpoints

The FastAPI backend exposes the following endpoints:

| Endpoint                  | Method | Description                                           |
| ------------------------- | ------ | ----------------------------------------------------- |
| `/`                       | GET    | Serves the React frontend (from `web/dist/` if built) |
| `/api/debate/stream`      | POST   | Starts a debate and streams events via SSE            |
| `/api/health`             | GET    | Health check — returns the current model name         |
| `/api/history`            | GET    | Lists all saved debate transcripts                    |
| `/api/history/{filename}` | GET    | Returns the content of a specific transcript          |

### Starting a Debate

```
POST /api/debate/stream
Content-Type: application/json

{
  "topic": "MoE vs Dense Models",
  "field": "Distributed Training"
}
```

The response is a Server-Sent Events (SSE) stream emitting the following event types:

| Event           | Description                                       |
| --------------- | ------------------------------------------------- |
| `status`        | Status messages (starting, loading, etc.)         |
| `professors`    | Professor panel data (names, roles, universities) |
| `round`         | Round number                                      |
| `speaker_start` | A professor is about to speak                     |
| `chunk`         | Streamed text chunk from a professor's response   |
| `speaker_end`   | Turn completed (includes fact-check tags)         |
| `moderator`     | Moderator summary                                 |
| `final`         | Final debate summary                              |
| `research_kit`  | Full research analysis output                     |
| `saved`         | Transcript saved confirmation                     |
| `error`         | Error message                                     |

---

## Frontend Features

- **Topic Library** — Browse pre-defined research topics by field
- **History Panel** — View and reload previous debate sessions
- **Professor Cards** — Color-coded by role (Empiricist, Theorist, Skeptic, Pragmatist, Historian)
- **Real-time Streaming** — Watch professor responses appear word by word
- **Fact-Check Tags** — Visual indicators for verified, unverified, contested, and opinion claims
- **Dark Mode** — Default dark theme
- **Responsive** — Works on desktop and mobile

---

## Tech Stack

| Layer     | Technology               |
| --------- | ------------------------ |
| Frontend  | React 18, Vite           |
| Backend   | FastAPI, Uvicorn         |
| Streaming | Server-Sent Events (SSE) |
| Styling   | CSS (custom)             |
| Build     | Vite                     |
