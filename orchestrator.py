import json
import re
import time
from debate.session import DebateSession, ProfessorProfile
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


def _call_gemini(prompt: str, max_tokens: int = 1000) -> str:
    try:
        from google import genai
    except ImportError:
        raise ImportError("google-genai not installed. Run: pip install google-genai")
    
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    def do():
        return client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": max_tokens, "temperature": 0.7},
        ).text.strip()
    return _retry(do)


# Roles selected automatically based on NUM_PROFESSORS
_ROLES = ["Empiricist", "Theorist", "Skeptic", "Pragmatist", "Historian"]

# Top universities in the US by field
_UNIVERSITIES = {
    "default":    ["MIT", "Stanford University", "Carnegie Mellon University",
                   "UC Berkeley", "University of Washington"],
    "llm":        ["MIT CSAIL", "Stanford AI Lab", "CMU LTI",
                   "UC Berkeley BAIR", "University of Washington NLP"],
    "systems":    ["MIT CSAIL", "Stanford InfoLab", "CMU SCS",
                   "UC Berkeley RISELab", "University of Illinois Urbana-Champaign"],
    "vision":     ["MIT CSAIL", "Stanford Vision Lab", "CMU Robotics Institute",
                   "UC Berkeley BAIR", "Georgia Tech"],
    "robotics":   ["MIT CSAIL", "Stanford AI Lab", "CMU Robotics Institute",
                   "UC San Diego", "University of Michigan"],
    "security":   ["MIT CSAIL", "Stanford Security Lab", "CMU CyLab",
                   "UC Berkeley", "Georgia Tech"],
}

def _pick_universities(field: str, n: int) -> list[str]:
    """Pick n universities appropriate for the research field."""
    field_lower = field.lower()
    key = "default"
    if any(w in field_lower for w in ["llm", "language", "nlp", "transformer"]):
        key = "llm"
    elif any(w in field_lower for w in ["system", "distributed", "efficient", "hardware"]):
        key = "systems"
    elif any(w in field_lower for w in ["vision", "image", "cv"]):
        key = "vision"
    elif any(w in field_lower for w in ["robot"]):
        key = "robotics"
    elif any(w in field_lower for w in ["security", "privacy", "crypto"]):
        key = "security"
    pool = _UNIVERSITIES[key]
    # Nếu cần nhiều hơn pool, lấy thêm từ default
    combined = pool + [u for u in _UNIVERSITIES["default"] if u not in pool]
    return combined[:n]


def generate_professors(topic: str, field: str) -> list[ProfessorProfile]:
    n = max(2, min(5, config.NUM_PROFESSORS))
    roles = _ROLES[:n]
    universities = _pick_universities(field, n)

    # Build list of slots for AI to fill in
    slots = []
    for i, (role, uni) in enumerate(zip(roles, universities)):
        key = f"prof_{chr(97+i)}"  # prof_a, prof_b, ...
        slots.append(f'  {{"key":"{key}","name":"Prof. [Last Name]","university":"{uni}","role":"{role}","personality":"[personality]","stance":"[specific stance on topic]","expertise":"[expertise]"}}')

    template = "[\n" + ",\n".join(slots) + "\n]"

    prompt = f"""You are assembling a PhD research seminar panel of {n} top US researchers.
Topic: "{topic}"
Field: {field}

These researchers will mathematically debate the hardest open problems in this field.
Fill in the JSON template below. Rules:
- name: realistic American academic name (e.g. "Prof. Hinton", "Prof. LeCun")
- personality: 1 short sentence describing their debate style (e.g. "Confronts opponents with counterexamples")
- stance: 1 specific sentence — their concrete MATHEMATICAL or METHODOLOGICAL approach to the key open problem in this field; name a specific technique, bound, or framework they advocate (not generic — never "evidence-based approach")
- expertise: their specific research specialization
- Each professor must have a DIFFERENT mathematical stance, roles are: {", ".join(roles)}
- The Skeptic must challenge the dominant approach's mathematical foundations directly
- Return ONLY the JSON array, no markdown, no extra text

{template}"""

    raw = _call_gemini(prompt, max_tokens=2000)
    raw = re.sub(r"```json|```", "", raw).strip()

    data = _parse_professors_json(raw, n)
    # Keep only correct fields, discard unknown fields, fill defaults if missing
    _DEFAULTS = {
        'key': 'prof_x',
        'name': 'Prof. Unknown',
        'university': 'MIT',
        'role': 'Empiricist',
        'personality': 'Debates analytically',
        'stance': 'Advocates evidence-based approach',
        'expertise': 'AI Research',
    }
    result = []
    for i, p in enumerate(data):
        merged = {**_DEFAULTS, 'key': f'prof_{chr(97+i)}'}
        merged.update({k: v for k, v in p.items() if k in _DEFAULTS})
        result.append(ProfessorProfile(**merged))
    return result


def generate_opening_question(topic: str, professors: list[ProfessorProfile]) -> str:
    names = ", ".join([f"{p.name} ({p.role})" for p in professors])
    prompt = f"""You are a Moderator of an academic debate.

Topic: "{topic}"
Professors: {names}

Write exactly 2 sentences:
Sentence 1: briefly introduce the topic and why it matters.
Sentence 2: invite {professors[0].name} to speak first."""
    return _call_gemini(prompt, max_tokens=150)


def create_session(topic: str, field: str) -> DebateSession:
    session = DebateSession(topic=topic, field=field)
    professors = generate_professors(topic, field)
    for p in professors:
        session.add_professor(p)
    return session


def _parse_professors_json(raw: str, expected: int) -> list[dict]:
    """Parse JSON flexibly - auto-fix common errors from smaller models."""
    raw = re.sub(r"```json|```", "", raw).strip()

    # Try direct parse
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass

    # Find all {...} objects and combine into array
    objects = re.findall(r'\{[^{}]+\}', raw, re.DOTALL)
    if objects:
        try:
            data = json.loads("[" + ",".join(objects) + "]")
            if isinstance(data, list) and len(data) >= 1:
                return data
        except json.JSONDecodeError:
            pass

    # Fallback - don't crash the program
    print("  [warn] JSON parse failed, using fallback professors", flush=True)
    roles = _ROLES[:expected]
    unis = _pick_universities("default", expected)
    return [
        {
            "key": f"prof_{chr(97+i)}",
            "name": f"Prof. {['Johnson','Williams','Brown','Davis','Miller'][i]}",
            "university": uni,
            "role": role,
            "personality": f"Debates from a {role.lower()} perspective",
            "stance": f"Advocates the {role.lower()} view on this topic",
            "expertise": "AI Research",
        }
        for i, (role, uni) in enumerate(zip(roles, unis))
    ]
