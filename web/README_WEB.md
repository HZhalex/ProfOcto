# ProfOcto Web UI — Setup Guide

## Requirements

- Node.js >= 18 (download from nodejs.org)
- Python 3.10+ with venv already setup (see main README)

## First Time — Install Node Packages

```bash
cd web
npm install
```

## Run (2 terminals in parallel)

**Terminal 1 — FastAPI Backend:**

```bash
# From project root
python -m venv .venv  # if not already created
.venv\Scripts\activate  # Windows
# or: source .venv/bin/activate  # macOS/Linux
uvicorn web.server:app --reload --port 8000
```

**Terminal 2 — React Frontend:**

```bash
cd web
npm run dev
```

Open browser: http://localhost:5173

## Build for Production

```bash
cd web
npm run build
```

After building, FastAPI will serve the React frontend from `web/dist/` directory.
