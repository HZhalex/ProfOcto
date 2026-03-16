# Debugging Guide - Academic Debate Arena

## Problem: Debate không hiển thị khi chạy

Khi bạn bắt đầu một cuộc tranh luận, giao diện vẫn sạch trắng hoặc không show nội dung.

## Nguyên nhân có thể

1. **SSE Stream không được thiết lập**: API `/api/debate/stream` không hoạt động đúng
2. **Proxy Vite buffering**: Dev server có thể buffering responses
3. **Lỗi Python backend**: Exception trong logic tranh luận được catch silently
4. **Network/CORS issues**: Frontend không thể gọi backend API

## Cách kiểm tra

### 1. Kiểm tra Backend Console

Khi bạn nhấn "Bắt đầu tranh luận", hãy xem terminal chạy uvicorn:

```
[API] /api/debate/stream called: <topic>
[Debate] Starting: <topic>
[Debate] Creating session...
[Debate] Session created with 2 professors
```

Nếu không thấy log này, có nghĩa **backend không nhận được request**.

### 2. Kiểm tra Browser Console

Nhấn F12 để mở Developer Tools, tab Console:

- Nếu thấy `[Fetch error]` → API endpoint not found hoặc không khả dụng
- Nếu thấy `[SSE] Invalid message format` → dữ liệu từ server có vấn đề
- Nếu thấy `[API error]` → Server trả về HTTP error code

### 3. Kiểm tra Network Tab (F12)

- Tìm request đến `/api/debate/stream`
- Xem Response Type - phải là `text/event-stream`
- Xem Preview để xem nội dung SSE events

## Các bước sửa lỗi

### Step 1: Đảm bảo Backend chạy

```powershell
# Terminal 1 - chạy backend
cd d:\project\academic_debate_arena
uvicorn web.server:app --reload --port 8000
```

### Step 2: Đảm bảo Frontend chạy

```powershell
# Terminal 2 - chạy dev server
cd d:\project\academic_debate_arena\web
npm run dev
```

### Step 3: Test API trực tiếp

Trước khi test UI, test xem API có work không:

Trong Python console:

```python
import json
import sys
sys.path.insert(0, 'd:\\project\\academic_debate_arena')

import config
from orchestrator import create_session, generate_opening_question

topic = "Diffusion Models vs Autoregressive Models"
field = "Machine Learning"

# Test session creation
session = create_session(topic, field)
print(f"✓ Session created with {len(session.professors)} professors")

# Test opening generation
opening = generate_opening_question(topic, session.professors)
print(f"✓ Opening generated: {len(opening)} chars")
```

Nếu hai dòng này thành công, backend logic OK.

### Step 4: Kiểm tra kết nối API proxy

Trong Python:

```python
from urllib.request import urlopen
import json

# Test API health
try:
    response = urlopen('http://localhost:8000/api/health')
    print(json.loads(response.read()))
except Exception as e:
    print(f"Backend not reachable: {e}")
```

### Step 5: Kiểm tra config

File `config.py` - đảm bảo các thiết lập:

```python
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")  # Phải có key!
NUM_PROFESSORS = 2      # Min 2, Max 5
MAX_ROUNDS = 2          # Ít nhất 1
MAX_TOKENS_PER_TURN = 400
FACT_CHECK_ENABLED = True
```

**Quan trọng**: Phải có API key cho Gemini để hoạt động!

## Log Messages Cần Biết

Backend logs (trong terminal uvicorn):

| Log                                          | Nghĩa                           |
| -------------------------------------------- | ------------------------------- |
| `[API] /api/debate/stream called`            | Request nhận được từ frontend ✓ |
| `[Debate] Starting`                          | Bắt đầu logic tranh luận ✓      |
| `[Debate] Creating session`                  | Tạo session                     |
| `[Debate] Session created with N professors` | ✓ Giáo sư tạo thành công        |
| `[Debate] Round 1`                           | Bắt đầu vòng 1                  |
| `[Debate] <Prof name> speaking (turn N)`     | Người nói được xác định         |
| `[Debate] Completed successfully`            | ✓ Tranh luận xong               |
| `[Debate FATAL ERROR]`                       | ✗ Lỗi nghiêm trọng              |

Frontend logs (F12 Console):

| Log                   | Nghĩa                   |
| --------------------- | ----------------------- |
| `[SSE] status`        | Nhận được status update |
| `[SSE] professors`    | Nhận danh sách giáo sư  |
| `[SSE] speaker_start` | Người nói bắt đầu       |
| `[SSE] chunk`         | Nhận nội dung chunk     |
| `[SSE] speaker_end`   | Người nói xong          |
| `[Fetch error]`       | ✗ API không thể reach   |
| `[Reader error]`      | ✗ Stream bị ngắt        |

## Nếu vẫn không hoạt động

1. **Kiểm tra .env file**
   - File `.env` ở thư mục gốc có GEMINI_API_KEY?
   - Test API key ở https://ai.google.dev

2. **Khởi động lại servers**

   ```powershell
   # Kill all
   Get-Process python | Stop-Process
   Get-Process node | Stop-Process

   # Restart từ đầu
   ```

3. **Check file paths**
   - Transcripts folder tồn tại? `d:\project\academic_debate_arena\transcripts\`
   - Prompts folder tồn tại? `d:\project\academic_debate_arena\prompts\`

4. **Kiểm tra dependencies**

   ```powershell
   cd d:\project\academic_debate_arena
   pip list | grep -E 'fastapi|google-genai'

   cd web
   npm list | head -20
   ```

## Cách test đơn giản nhất

Terminal 1:

```powershell
cd d:\project\academic_debate_arena
python main.py
```

Nếu `main.py` chạy xong không lỗi, thì backend logic OK. Lỗi sẽ là ở SSE streaming hoặc frontend.

---

**Sau khi fix, hãy:**

1. Xóa brower cache (Ctrl+Shift+Delete)
2. Hard refresh (Ctrl+Shift+R)
3. Kiểm tra browser console lần nữa
