<div align="center">

# ⚔️ Academic Debate Arena

**Học qua tranh luận giữa các giáo sư AI hàng đầu thế giới**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![Gemini](https://img.shields.io/badge/Gemini_API-Free_Tier-4285F4?style=flat-square&logo=google&logoColor=white)](https://aistudio.google.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## ⚡ Tổng quan

**Academic Debate Arena** là một hệ thống học tập thông qua tranh luận học thuật giữa các AI agents đóng vai giáo sư quốc tế. Người dùng chỉ cần nhập một topic nghiên cứu — hệ thống tự động tạo ra một panel các giáo sư hàng đầu từ MIT, Stanford, CMU... với quan điểm đối lập nhau, tranh luận gay gắt, và fact-check lẫn nhau theo thời gian thực.

> *Tại sao học qua tranh luận? Vì não bộ tiếp thu thông tin hiệu quả hơn nhiều khi phải xử lý nhiều góc nhìn mâu thuẫn nhau cùng lúc.*

### 🚀 4 điểm khác biệt chính

1. **Professors tự động theo lĩnh vực** — Nhập topic về Distributed LLM thì ra MIT CSAIL, Stanford AI Lab. Nhập về Computer Vision thì ra CMU Robotics, Berkeley BAIR. Không hardcode sẵn.

2. **Fact-checker tích hợp Google Search** — Mỗi claim của professor được tự động kiểm chứng bằng web search thật, gắn tag `VERIFIED` / `CONTESTED` / `OPINION` ngay bên dưới lượt nói.

3. **Streaming real-time như ChatGPT** — Web UI hiển thị từng chữ xuất hiện, không phải chờ cả đoạn. Sidebar hiển thị professors, fact tags, key insights.

4. **Topic Library có sẵn** — 19 topic chất lượng cao phân theo 5 lĩnh vực AI, click là chạy ngay. Lịch sử tranh luận được lưu lại để đọc sau.

---

## 🏗️ Kiến trúc hệ thống

```
User Input
    │
    ▼
Orchestrator ──── tự sinh professors phù hợp với lĩnh vực
    │
    ▼
┌───────────────────────────────────────┐
│           Professor Panel             │
│  Empiricist │ Theorist │ Skeptic │ …  │
└───────────────────────────────────────┘
    │                         │
    ▼                         ▼
Moderator Agent          Fact-Checker Agent
(tóm tắt, câu hỏi mới)  (Google Search + tag claim)
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
├── main.py                      # Entry point — Terminal UI
├── config.py                    # Cấu hình toàn bộ hệ thống
├── orchestrator.py              # Tạo professors + câu hỏi mở màn
│
├── agents/
│   ├── professor.py             # Professor agent — generate lượt nói
│   ├── moderator.py             # Tóm tắt round + key insights cuối
│   └── fact_checker.py          # Web search + gắn tag claim
│
├── debate/
│   ├── session.py               # State: professors, turns, history
│   └── turn_manager.py          # Quản lý thứ tự, phát hiện lặp lại
│
├── output/
│   ├── terminal_renderer.py     # Rich terminal — màu sắc, panel
│   └── exporter.py              # Export Markdown + PDF
│
├── prompts/
│   ├── professor_base.txt       # System prompt professor
│   ├── moderator.txt            # System prompt moderator
│   └── fact_checker.txt         # System prompt fact-checker
│
├── web/
│   ├── server.py                # FastAPI + SSE streaming
│   └── src/
│       ├── App.jsx              # React UI
│       └── topics.js            # Topic library data
│
└── transcripts/                 # Transcript .md tự động lưu
```

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
```

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

| Tham số | Mặc định | Ý nghĩa |
|---------|----------|---------|
| `MODEL` | `gemma-3-1b-it` | Model Gemini đang dùng |
| `NUM_PROFESSORS` | `4` | Số giáo sư (2–5) |
| `MAX_ROUNDS` | `2` | Số vòng tranh luận |
| `MAX_TURNS_PER_ROUND` | `1` | Số lượt nói/professor/round |
| `MAX_TOKENS_PER_TURN` | `400` | Độ dài tối đa mỗi lượt |
| `FACT_CHECK_ENABLED` | `True` | Bật/tắt fact-checker |
| `STREAM_OUTPUT` | `True` | Stream text real-time |
| `SAVE_TRANSCRIPT` | `True` | Lưu transcript .md |

### Chọn model

| Model | Free tier | Chất lượng | Tốc độ |
|-------|-----------|------------|--------|
| `gemma-3-1b-it` | ✅ Không giới hạn | ⭐⭐ | ⚡⚡⚡ |
| `gemini-1.5-flash` | ✅ 15 req/phút | ⭐⭐⭐⭐ | ⚡⚡ |
| `gemini-2.5-flash` | ✅ 5 req/phút | ⭐⭐⭐⭐⭐ | ⚡ |

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