<div align="center">

# ⚔️ Academic Debate Arena

**AI-Powered Research Gap Discovery for PhD Students**

Research smarter by debating with multiple AI professors, identifying ICLR-ready gaps, and sharing with your advisor.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini_API-Free_Tier-4285F4?style=flat-square&logo=google&logoColor=white)](https://aistudio.google.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## 🎯 Quick Start

```bash
# 1. Setup (2 min)
echo "GEMINI_API_KEY=your-key" > .env
pip install -r requirements.txt

# 2. Run (5 min)
python main.py

# 3. Explore
[dashboard shows top gap]
[bookmark / export / pitch options]
```

**Full guide:** See [Quick Start Guide](docs/guides/01_QUICK_START.md)

---

## 📚 Documentation

All documentation is organized in the **`docs/`** folder:

### Getting Started

- **[Quick Start](docs/guides/01_QUICK_START.md)** — 5-minute setup
- **[Phase 7 User Guide](docs/guides/03_PHASE7_USER_GUIDE.md)** — All 7 new features (bookmarking, PDF export, elevator pitch, etc.)

### Features & How They Work

- **[Config Reference](docs/development/CONFIG_REFERENCE.md)** — 100+ configuration flags
- **[Phase 5: ICLR Pipeline](docs/features/PHASE5_ICLR_PIPELINE.md)** — Readiness scoring
- **[Phase 7 Report](docs/features/PHASE7_COMPLETION_REPORT.md)** — Implementation details

### Troubleshooting

- **[Debugging Guide](docs/development/DEBUGGING.md)** — Common issues & logs

**[→ View all docs](docs/README.md)**

---

## ✨ Features (Phase 7)

(tóm tắt, câu hỏi mới) (Google Search + tag claim)
│
▼
Output Layer
├── Terminal (Rich UI)
├── Web UI (React + SSE streaming)
└── Transcript (.md export)

```

### Cấu trúc thư mục

```

academic_debate_arena/
├── main.py # Entry point — Terminal UI
├── config.py # Cấu hình toàn bộ hệ thống
├── orchestrator.py # Tạo professors + câu hỏi mở màn
│
├── agents/
│ ├── professor.py # Professor agent — generate lượt nói
│ ├── moderator.py # Tóm tắt round + key insights cuối
│ └── fact_checker.py # Web search + gắn tag claim
│
├── debate/
│ ├── session.py # State: professors, turns, history
│ └── turn_manager.py # Quản lý thứ tự, phát hiện lặp lại
│
├── output/
│ ├── terminal_renderer.py # Rich terminal — màu sắc, panel
│ └── exporter.py # Export Markdown + PDF
│
├── prompts/
│ ├── professor_base.txt # System prompt professor
│ ├── moderator.txt # System prompt moderator
│ └── fact_checker.txt # System prompt fact-checker
│
├── web/
│ ├── server.py # FastAPI + SSE streaming
│ └── src/
│ ├── App.jsx # React UI
│ └── topics.js # Topic library data
│
└── transcripts/ # Transcript .md tự động lưu

````

---

## 🚀 Quick Start

### Yêu cầu

- Python 3.10+
- Node.js 18+ (chỉ cần cho Web UI)
- Gemini API key (miễn phí tại [aistudio.google.com](https://aistudio.google.com))

### 1. Cài đặt

```bash
# Clone hoặc giải nén project
cd academic_debate_arena

# Tạo virtual environment
python -m venv .venv

# Windows
.venv\Scripts\pip install -r requirements.txt

# macOS / Linux
.venv/bin/pip install -r requirements.txt
````

### 2. Cấu hình API Key

```bash
# Copy file mẫu
cp .env.example .env

# Mở .env và điền key
GEMINI_API_KEY=AIza...your_key_here...
```

Lấy key miễn phí tại: [aistudio.google.com](https://aistudio.google.com) → **Get API key** → **Create API key**

### 3a. Chạy Terminal UI

```bash
# Windows
.venv\Scripts\activate
python main.py

# macOS / Linux
source .venv/bin/activate
python main.py

# Hoặc truyền thẳng argument
python main.py "MoE vs Dense: trade-off nào tốt hơn cho production?" "Distributed LLM"
```

### 3b. Chạy Web UI

Cài Node packages (lần đầu):

```bash
cd web
npm install
```

Mở **2 terminal song song**:

```bash
# Terminal 1 — Backend
.venv\Scripts\activate
uvicorn web.server:app --reload --port 8000

# Terminal 2 — Frontend
cd web
npm run dev
```

Mở trình duyệt: **http://127.0.0.1:3000**

---

## ⚙️ Cấu hình

Tất cả tham số chỉnh trong `config.py`:

| Tham số               | Mặc định        | Ý nghĩa                     |
| --------------------- | --------------- | --------------------------- |
| `MODEL`               | `gemma-3-1b-it` | Model Gemini đang dùng      |
| `NUM_PROFESSORS`      | `4`             | Số giáo sư (2–5)            |
| `MAX_ROUNDS`          | `2`             | Số vòng tranh luận          |
| `MAX_TURNS_PER_ROUND` | `1`             | Số lượt nói/professor/round |
| `MAX_TOKENS_PER_TURN` | `400`           | Độ dài tối đa mỗi lượt      |
| `FACT_CHECK_ENABLED`  | `True`          | Bật/tắt fact-checker        |
| `STREAM_OUTPUT`       | `True`          | Stream text real-time       |
| `SAVE_TRANSCRIPT`     | `True`          | Lưu transcript .md          |

### Chọn model

| Model              | Free tier         | Chất lượng | Tốc độ |
| ------------------ | ----------------- | ---------- | ------ |
| `gemma-3-1b-it`    | ✅ Không giới hạn | ⭐⭐       | ⚡⚡⚡ |
| `gemini-1.5-flash` | ✅ 15 req/phút    | ⭐⭐⭐⭐   | ⚡⚡   |
| `gemini-2.5-flash` | ✅ 5 req/phút     | ⭐⭐⭐⭐⭐ | ⚡     |

---

## 💡 Cách dùng hiệu quả

**Chỉnh prompt** — Mở file trong `prompts/` để thay đổi tính cách professors, cách moderator tóm tắt, tiêu chí fact-check mà không cần sửa code.

**Topic Library** — Trên Web UI, tab "📚 Library" có sẵn 19 topic chất lượng cao phân theo 5 lĩnh vực. Click chọn → nhấn Start là chạy ngay.

**Export PDF** — Cài thêm `pip install reportlab` rồi gọi `exporter.export_pdf(session)` để xuất transcript ra PDF có formatting đẹp.

---

## ✅ Roadmap

- [x] Phase 1 — Terminal MVP: professors, moderator, fact-checker, transcript
- [x] Phase 2 — Web search fact-check, professors quốc tế theo lĩnh vực
- [x] Phase 3 — Web UI React + SSE streaming real-time
- [x] Phase 4 — Topic library, session history, turn manager, exporter

---

## ⚠️ Lưu ý

- Project này dùng cho mục đích học tập cá nhân.
- Gemini free tier có giới hạn requests/phút — hệ thống tự động retry khi bị rate limit.
- Fact-check bằng AI không đảm bảo 100% chính xác — luôn verify lại các claim quan trọng từ nguồn gốc.
- Với `gemma-3-1b-it` (model nhỏ), chất lượng tranh luận sẽ kém hơn — khuyến khích dùng `gemini-1.5-flash` để có kết quả tốt hơn.

---

## 📄 License

MIT License — tự do sử dụng và chỉnh sửa cho mục đích cá nhân và học tập.
