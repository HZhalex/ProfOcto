import re
import time
from google import genai
from google.genai import errors as genai_errors
from debate.session import DebateSession
from prompts import load_system, load_template
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
            config={"max_output_tokens": max_tokens, "temperature": 0.5,
                    "stop_sequences": ["\n\n\n\n"]},
        ).text.strip()
    return _retry(do)


def generate_moderator_summary(session: DebateSession) -> str:
    system = load_system("moderator")
    history = session.get_history_text(max_turns=3)
    prompt = f"""{system}

Topic: "{session.topic}" | Round {session.current_round} just ended.

RECENT DEBATE:
{history}

Write exactly 3 sentences in Vietnamese:
1. The biggest point of disagreement.
2. Who made the most compelling argument and why.
3. A new question to deepen the debate."""
    return _call(prompt, max_tokens=200)


def generate_final_summary(session: DebateSession) -> str:
    system = load_system("moderator")
    history = session.get_history_text(max_turns=6)
    prompt = f"""{system}

Topic: "{session.topic}"

DEBATE:
{history}

Summarize in Vietnamese using this exact format, 1-2 lines each:

Đồng thuận: [write here]
Bất đồng: [write here]
Câu hỏi mở: [write here]
Nghiên cứu tiếp: [write here]"""
    return _call(prompt, max_tokens=300)
