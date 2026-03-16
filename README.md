# Academic Debate Arena

Học qua tranh luận giữa các giáo sư AI về bất kỳ topic nào.

## Cài đặt

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
```

## Chạy

```bash
# Interactive mode (được hỏi topic)
python main.py

# Truyền thẳng argument
python main.py "MoE vs Dense models ở production scale" "Distributed LLM"
```

## Cấu trúc project

```
academic_debate_arena/
├── main.py                  # Entry point
├── config.py                # Cấu hình: model, max_turns, fact_check...
├── orchestrator.py          # Tạo professors, generate opening
├── agents/
│   ├── professor.py         # Professor agent — generate lượt nói
│   ├── moderator.py         # Moderator — tóm tắt & câu hỏi mới
│   └── fact_checker.py      # Fact-checker — gắn tag claim
├── debate/
│   └── session.py           # State: professors, turns, history, export
├── output/
│   └── terminal_renderer.py # Rich terminal UI
└── transcripts/             # File .md được lưu tại đây
```

## Tuỳ chỉnh trong config.py

| Tham số | Mặc định | Ý nghĩa |
|---------|----------|---------|
| `MAX_TURNS_PER_ROUND` | 2 | Mỗi professor nói bao nhiêu lần/round |
| `MAX_ROUNDS` | 3 | Số rounds tổng |
| `MAX_TOKENS_PER_TURN` | 400 | Độ dài tối đa mỗi lượt nói |
| `FACT_CHECK_ENABLED` | True | Bật/tắt fact-checker |
| `STREAM_OUTPUT` | True | Stream text real-time |
| `SAVE_TRANSCRIPT` | True | Lưu file markdown |

## Roadmap

- [x] Phase 1: MVP — Terminal, 4 professors, moderator, fact-checker
- [x] Phase 2: Web search fact-check (Brave/Tavily API)
- [x] Phase 3: Web UI (FastAPI + SSE streaming)
- [ ] Phase 4: Session replay, topic library
