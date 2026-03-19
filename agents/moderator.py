import re
import time
from debate.session import DebateSession
from prompts import load_system, load_template
import config


def _retry(fn, max_retries: int = 2):
    """Retry with minimal delays to avoid hanging."""
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:  # Broad exception for API errors
            if attempt < max_retries - 1:
                import time
                time.sleep(0.5)  # Short fixed delay instead of exponential
            else:
                raise


def _call(prompt: str, max_tokens: int) -> str:
    try:
        from google import genai
    except ImportError:
        raise ImportError("google-genai not installed. Run: pip install google-genai")
    
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

Topic: "{session.topic}" | Field: {session.field} | Round {session.current_round} just ended.

RECENT EXCHANGE:
{history}

Write exactly 3 sentences in English:
1. The specific mathematical claim or approach proposed, and whether it formally holds given its stated conditions.
2. The sharpest unresolved flaw, missing condition, or open sub-problem remaining in the argument.
3. One targeted question attacking the weakest formal assumption just made."""
    return _call(prompt, max_tokens=200)


def generate_final_summary(session: DebateSession) -> str:
    system = load_system("moderator")
    history = session.get_history_text(max_turns=6)
    prompt = f"""{system}

Topic: "{session.topic}" | Field: {session.field}

FULL DEBATE:
{history}

Summarize in English using this exact format, 1-2 lines each:

Open Gaps: [which research gaps were precisely identified in the debate]
Proposed Approaches: [formal mathematical approaches proposed, with their key conditions or requirements]
Unresolved: [what mathematical questions remain open after this debate]
Most Tractable: [which problem is closest to formal resolution based on the arguments made]"""
    return _call(prompt, max_tokens=300)
