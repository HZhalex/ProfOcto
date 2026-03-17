import json
import re
import time
import config


def _retry(fn, max_retries: int = 2, initial_wait: float = 0.5):
    """Retry with short delays. Fail fast to avoid hanging."""
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            if attempt < max_retries - 1:
                import time
                time.sleep(initial_wait)  # Short fixed delay
            else:
                # Fail fast instead of returning empty
                return []


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

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("  [fact-check] google-genai not installed, skipping fact check")
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
                    timeout=5.0,  # 5 second timeout
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                ),
            )

        response = _retry(do, max_retries=1)  # Only 1 attempt, fail fast
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

    except Exception as e:
        # Fail fast — don't block debate with timeout/retry
        print(f"    [fact-check] skipped ({type(e).__name__})", flush=True)
        return []
