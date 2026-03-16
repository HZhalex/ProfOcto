import json
import re
import time
from google import genai
from google.genai import errors as genai_errors
from debate.session import DebateSession, ProfessorProfile
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


def _call_gemini(prompt: str, max_tokens: int = 1000) -> str:
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    def do():
        return client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": max_tokens, "temperature": 0.7},
        ).text.strip()
    return _retry(do)


# Roles được chọn tự động theo NUM_PROFESSORS
_ROLES = ["Empiricist", "Theorist", "Skeptic", "Pragmatist", "Historian"]

# Các trường top ở Mỹ theo lĩnh vực
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
    """Chọn n trường phù hợp với lĩnh vực."""
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

    # Build danh sách slot để AI điền vào
    slots = []
    for i, (role, uni) in enumerate(zip(roles, universities)):
        key = f"prof_{chr(97+i)}"  # prof_a, prof_b, ...
        slots.append(f'  {{"key":"{key}","name":"Prof. [Last Name]","university":"{uni}","role":"{role}","personality":"[personality]","stance":"[specific stance on topic]","expertise":"[expertise]"}}')

    template = "[\n" + ",\n".join(slots) + "\n]"

    prompt = f"""You are designing an academic debate panel of {n} US professors.
Topic: "{topic}"
Field: {field}

Fill in the JSON template below. Rules:
- name: realistic American academic name (e.g. "Prof. Hinton", "Prof. LeCun")
- personality: 1 short sentence describing debate style
- stance: 1 specific sentence — their concrete position ON THIS TOPIC (not generic)
- expertise: their specific research area
- Each professor must have a DIFFERENT stance, roles are: {", ".join(roles)}
- The Skeptic must strongly challenge the mainstream view
- Return ONLY the JSON array, no markdown, no extra text

{template}"""

    raw = _call_gemini(prompt, max_tokens=2000)
    raw = re.sub(r"```json|```", "", raw).strip()

    data = _parse_professors_json(raw, n)
    # Chỉ lấy đúng fields, bỏ field lạ, điền default nếu thiếu
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
    prompt = f"""You are a Moderator of an academic debate. Write in Vietnamese.

Topic: "{topic}"
Professors: {names}

Write exactly 2 sentences in Vietnamese:
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
    """Parse JSON linh hoạt — tự sửa các lỗi phổ biến của model nhỏ."""
    raw = re.sub(r"```json|```", "", raw).strip()

    # Thử parse thẳng
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass

    # Tìm tất cả objects {...} rồi ghép thành array
    objects = re.findall(r'\{[^{}]+\}', raw, re.DOTALL)
    if objects:
        try:
            data = json.loads("[" + ",".join(objects) + "]")
            if isinstance(data, list) and len(data) >= 1:
                return data
        except json.JSONDecodeError:
            pass

    # Fallback — không crash chương trình
    print("  [warn] JSON parse thất bại, dùng fallback professors", flush=True)
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