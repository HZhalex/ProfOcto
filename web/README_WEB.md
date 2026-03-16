# Web UI — Hướng dẫn chạy

## Yêu cầu
- Node.js >= 18 (tải tại nodejs.org)
- Python venv đã setup (xem README chính)

## Lần đầu — cài Node packages

```cmd
cd web
npm install
```

## Chạy (2 terminal song song)

**Terminal 1 — FastAPI backend:**
```cmd
cd D:\project\academic_debate_arena
.venv\Scripts\activate
uvicorn web.server:app --reload --port 8000
```

**Terminal 2 — React frontend:**
```cmd
cd D:\project\academic_debate_arena\web
npm run dev
```

Mở trình duyệt: http://localhost:5173

## Build production (optional)

```cmd
cd web
npm run build
```
Sau khi build, FastAPI tự serve React từ `web/dist/`.
