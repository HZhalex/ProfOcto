import os

# Tự động đọc .env nếu có
_env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

MODEL = "gemma-3-1b-it"

# Debate settings
NUM_PROFESSORS = 2    # số giáo sư, min 2 max 5
MAX_TURNS_PER_ROUND = 1
MAX_ROUNDS = 1
MAX_TOKENS_PER_TURN = 400
FACT_CHECK_ENABLED = True
LANGUAGE = "vi"

# Research Mode (khi ON: generate research kit + paper outline sau debate)
RESEARCH_MODE = True  # Bật research synthesis + paper outline
RESEARCH_MAX_RECOMMENDATIONS = 5

# Academic Rigor Mode (khi ON: professors must back claims with theorems + citations)
ACADEMIC_RIGOR_MODE = True  # Enforce mathematical backing in debates

# Display
STREAM_OUTPUT = True
SAVE_TRANSCRIPT = True
TRANSCRIPT_DIR = "transcripts"
RESEARCH_KIT_DIR = "research_kits"  # Nơi lưu research kits
