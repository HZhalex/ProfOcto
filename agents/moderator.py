import re
import time
from google import genai
from google.genai import errors as genai_errors
from debate.session import DebateSession
import config


def _retry(fn, max_retries: int = 5):
    for attempt in range(max_retries):
        try:
            return fn()
        except genai_errors.ClientError as e:
            if e.status_code == 429 and attempt < max_retries - 1:
                wait = 60
                m = re.search(r'retry in (\d+)', str(e), re.IGNORECASE)
                if m:
                    wait = int(m.group(1)) + 3
                print(f"\n  [rate limit] chờ {wait}s rồi thử lại...", flush=True)
                time.sleep(wait)
            else:
                raise


def _call(prompt: str, max_tokens: int) -> str:
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    def do():
        return client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={
                "max_output_tokens": max_tokens,
                "temperature": 0.5,
                "stop_sequences": ["\n\n\n\n"],
            },
        ).text.strip()
    return _retry(do)


def generate_moderator_summary(session: DebateSession) -> str:
    # Lấy tối đa 3 turns gần nhất — model nhỏ không cần nhiều hơn
    history = session.get_history_text(max_turns=3)
    prompt = f"""Bạn là Moderator. Topic: "{session.topic}"

Các giáo sư vừa tranh luận:
{history}

Viết đúng 3 câu bằng tiếng Việt:
1. Điểm bất đồng lớn nhất là gì.
2. Ai có lập luận thuyết phục nhất và tại sao.
3. Câu hỏi mới để tiếp tục tranh luận."""
    return _call(prompt, max_tokens=200)


def generate_final_summary(session: DebateSession) -> str:
    # Chỉ lấy 6 turns cuối để tránh context quá dài gây loop
    history = session.get_history_text(max_turns=6)
    prompt = f"""Bạn là Moderator. Topic: "{session.topic}"

Tranh luận:
{history}

Tóm tắt ngắn gọn bằng tiếng Việt theo đúng format sau, mỗi mục chỉ 1-2 dòng:

Đồng thuận: [viết ở đây]
Bất đồng: [viết ở đây]
Câu hỏi mở: [viết ở đây]
Nghiên cứu tiếp: [viết ở đây]"""
    return _call(prompt, max_tokens=300)
