import re
import time
from google import genai
from google.genai import errors as genai_errors
from debate.session import DebateSession, ProfessorProfile
import config


def _call_with_retry(fn, max_retries: int = 5):
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


def generate_professor_turn(
    prof: ProfessorProfile,
    session: DebateSession,
    stream_callback=None,
) -> str:
    client = genai.Client(api_key=config.GEMINI_API_KEY)

    # Lấy chỉ lượt nói CUỐI CÙNG để model nhỏ không bị overwhelm
    last_turn = session.get_history_text(max_turns=2)

    # Fix 1: Prompt cực ngắn cho model nhỏ
    # Fix 2: Bắt buộc PHẢN BÁC, không cho phép đồng ý
    prompt = f"""Bạn là {prof.name} ({prof.role}), quan điểm: {prof.stance}

Người vừa nói: {last_turn}

Hãy PHẢN BÁC quan điểm trên. Chỉ viết 3 câu bằng tiếng Việt. KHÔNG bắt đầu bằng "Tôi đồng ý". KHÔNG lặp lại những gì đã nói."""

    # Fix 3: temperature thấp hơn + repetition_penalty để tránh loop
    gen_config = {
        "max_output_tokens": config.MAX_TOKENS_PER_TURN,
        "temperature": 0.7,
        "stop_sequences": ["\n\n\n"],  # dừng nếu bắt đầu lặp
    }

    if stream_callback:
        def do_stream():
            full_text = ""
            for chunk in client.models.generate_content_stream(
                model=config.MODEL,
                contents=prompt,
                config=gen_config,
            ):
                if chunk.text:
                    full_text += chunk.text
                    stream_callback(chunk.text)
            return full_text.strip()
        return _call_with_retry(do_stream)
    else:
        def do_call():
            return client.models.generate_content(
                model=config.MODEL,
                contents=prompt,
                config=gen_config,
            ).text.strip()
        return _call_with_retry(do_call)
