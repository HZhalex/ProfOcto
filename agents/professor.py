import re
import time
from debate.session import DebateSession, ProfessorProfile
from prompts import load_system
import config


def _is_primarily_english(text: str) -> bool:
    """Check if text is primarily in English (>40% English words).
    
    Vietnamese uses mostly non-ASCII characters. If we see lots of common 
    English words, it's probably English.
    """
    english_words = {
        'the', 'a', 'and', 'is', 'are', 'to', 'in', 'of', 'for', 'that',
        'this', 'with', 'but', 'be', 'have', 'not', 'as', 'from', 'by',
        'on', 'or', 'an', 'it', 'has', 'was', 'were', 'been', 'can',
        'would', 'could', 'should', 'do', 'does', 'did', 'will', 'which',
        'what', 'when', 'where', 'why', 'how', 'model', 'training',
        'data', 'algorithm', 'approach', 'method', 'research', 'however',
        'therefore', 'because', 'while', 'though', 'although', 'also',
        'more', 'most', 'less', 'some', 'other', 'different', 'our', 'we',
        'they', 'their', 'these', 'those', 'such', 'very', 'just', 'only',
        'about', 'new', 'good', 'best', 'use', 'used', 'using', 'way',
        'time', 'work', 'years', 'then', 'now', 'here', 'such', 'may'
    }
    
    # Extract words (lowercase, alphanumeric only)
    words = re.findall(r'\b[a-z]+\b', text.lower())
    if not words:
        return False
    
    english_count = sum(1 for w in words if w in english_words)
    english_ratio = english_count / len(words) if words else 0
    
    # Count consecutive English sequences (if we see 3+ English words in a row, likely English)
    english_word_sequences = re.findall(r'(?:\b[a-z]+\b\s+){2,}', text.lower())
    has_english_sequence = len(english_word_sequences) > 0
    
    # If >35% English words OR has English word sequences, consider it English
    return english_ratio > 0.35 or (has_english_sequence and english_ratio > 0.25)


def _call_with_retry(fn, max_retries: int = 2):
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


def generate_professor_turn(
    prof: ProfessorProfile,
    session: DebateSession,
    stream_callback=None,
) -> str:
    try:
        from google import genai
    except ImportError:
        raise ImportError("google-genai not installed. Run: pip install google-genai")
    
    client = genai.Client(api_key=config.GEMINI_API_KEY)

    # Load system prompt từ file (rigor mode or standard mode)
    system_prompt_name = "professor_rigor" if config.ACADEMIC_RIGOR_MODE else "professor"
    system = load_system(system_prompt_name,
        name=prof.name,
        university=prof.university,
        expertise=prof.expertise,
        personality=prof.personality,
        stance=prof.stance,
        professors_summary=session.get_professors_summary(),
    )

    last_turn = session.get_history_text(max_turns=3)
    
    # Try up to 2 times - first normally, second with stronger English enforcement
    for attempt in range(2):
        # Strengthen English requirement on retry
        extra_instruction = ""
        if attempt > 0:
            extra_instruction = "\n\n*** CRITICAL: Your previous response was not in English. You MUST respond ENTIRELY in English this time. No other languages allowed! ***"
        
        prompt = f"""{system}

Field: {session.field}
Topic: "{session.topic}"

RECENT EXCHANGE:
{last_turn}

Your turn — {prof.name}. Advance the mathematical argument on the open problem under discussion. English only.{extra_instruction}"""

        gen_config = {
            "max_output_tokens": config.MAX_TOKENS_PER_TURN,
            "temperature": 0.7 if attempt == 0 else 0.5,  # Lower temp on retry
            "stop_sequences": ["\n\n\n"],
        }

        full_text = ""
        try:
            if stream_callback:
                def do_stream():
                    nonlocal full_text
                    full_text = ""
                    for chunk in client.models.generate_content_stream(
                        model=config.MODEL, contents=prompt, config=gen_config,
                    ):
                        if chunk.text:
                            full_text += chunk.text
                            stream_callback(chunk.text)
                    return full_text.strip()
                result = _call_with_retry(do_stream)
            else:
                def do_call():
                    nonlocal full_text
                    response = client.models.generate_content(
                        model=config.MODEL, contents=prompt, config=gen_config,
                    )
                    full_text = response.text.strip()
                    return full_text
                result = _call_with_retry(do_call)
            
            # Check if response is primarily English (what we want)
            if _is_primarily_english(result):
                return result  # Good: English response
            else:
                print(f"[Lang Check] {prof.name}'s response detected as non-English, retrying with stronger instruction...", flush=True)
                # Loop to retry
                continue
        
        except Exception as e:
            print(f"[Professor] Error generating turn: {e}", flush=True)
            if attempt < 1:
                continue  # Try again
            else:
                raise  # Give up after 2 attempts
    
    # Fallback if both attempts still non-English
    print(f"[Lang Check] WARNING: {prof.name} still responding in non-English after retry", flush=True)
    return result  # Return it anyway
