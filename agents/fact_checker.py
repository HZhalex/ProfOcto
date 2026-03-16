import json
import re
import time
from google import genai
from google.genai import errors as genai_errors
from google.genai import types
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


def _extract_search_sources(response) -> list[str]:
    """Trích xuất nguồn URL từ grounding metadata của Gemini search."""
    sources = []
    try:
        candidate = response.candidates[0]
        grounding = candidate.grounding_metadata
        if grounding and grounding.grounding_chunks:
            for chunk in grounding.grounding_chunks:
                if hasattr(chunk, 'web') and chunk.web:
                    uri = getattr(chunk.web, 'uri', None)
                    title = getattr(chunk.web, 'title', None)
                    if uri:
                        sources.append(title or uri)
    except Exception:
        pass
    return sources[:3]  # tối đa 3 nguồn


def fact_check_turn(content: str, speaker_name: str) -> list[dict]:
    if not config.FACT_CHECK_ENABLED:
        return []

    client = genai.Client(api_key=config.GEMINI_API_KEY)

    # Bước 1: Dùng Gemini + Google Search để kiểm chứng
    search_prompt = f"""Kiểm chứng các claim trong phát biểu học thuật sau bằng cách tìm kiếm thông tin:

Phát biểu của {speaker_name}:
"{content}"

Hãy:
1. Xác định tối đa 3 claim quan trọng nhất (bỏ qua opinion)
2. Tìm kiếm để kiểm chứng từng claim
3. Trả về JSON array, không markdown, không text thừa:
[{{"claim": "mô tả ngắn tối đa 8 từ", "status": "VERIFIED|UNVERIFIED|CONTESTED|OPINION", "reason": "lý do 1 câu"}}]

Nếu không có claim đáng chú ý, trả về []"""

    try:
        def do():
            return client.models.generate_content(
                model=config.MODEL,
                contents=search_prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=400,
                    temperature=0.1,
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                ),
            )

        response = _retry(do)
        sources = _extract_search_sources(response)

        raw = response.text.strip()
        raw = re.sub(r"```json|```", "", raw).strip()

        # Parse JSON
        data = None
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            match = re.search(r'\[.*?\]', raw, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group())
                except Exception:
                    pass

        if not isinstance(data, list):
            return []

        # Gắn nguồn vào kết quả nếu có
        if sources:
            for item in data:
                if item.get("status") in ("VERIFIED", "CONTESTED"):
                    item["sources"] = sources

        return data

    except Exception:
        return []
