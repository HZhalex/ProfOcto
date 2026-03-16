"""
Research Synthesizer - Generate research kit từ debate sessions
Tạo paper outline, key findings, citations, và open questions
"""
import json
import re
from google import genai
from google.genai import errors as genai_errors
from debate.session import DebateSession
import config


def _retry(fn, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            return fn()
        except genai_errors.ClientError as e:
            if e.status_code == 429 and attempt < max_retries - 1:
                import time
                wait = 30
                m = re.search(r'retry in (\d+)', str(e), re.IGNORECASE)
                if m:
                    wait = int(m.group(1)) + 2
                time.sleep(wait)
            else:
                if attempt == max_retries - 1:
                    return None
                raise


def generate_research_kit(session: DebateSession, topic: str, field: str) -> dict:
    """
    Generate research kit từ debate session.
    Returns dict với: outline, key_findings, open_questions, citations
    """
    if not config.RESEARCH_MODE:
        return {}

    print(f"[Research] Synthesizing research kit for: {topic[:60]}", flush=True)
    
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    
    # 1. Tóm tắt debate để dùng làm context
    debate_summary = _build_debate_summary(session)
    
    # 2. Generate paper outline
    print("[Research] Generating paper outline...", flush=True)
    outline = _generate_paper_outline(client, topic, field, debate_summary)
    
    # 3. Extract key findings từ debate
    print("[Research] Extracting key findings...", flush=True)
    findings = _extract_key_findings(client, topic, session)
    
    # 4. Generate open questions
    print("[Research] Identifying open questions...", flush=True)
    open_questions = _generate_open_questions(client, topic, field, debate_summary)
    
    # 5. Extract research recommendations
    print("[Research] Generating research recommendations...", flush=True)
    recommendations = _generate_recommendations(client, topic, field, findings)
    
    kit = {
        "topic": topic,
        "field": field,
        "outline": outline,
        "key_findings": findings,
        "open_questions": open_questions,
        "recommendations": recommendations,
    }
    
    print("[Research] Research kit generated successfully", flush=True)
    return kit


def _build_debate_summary(session: DebateSession) -> str:
    """Tóm tắt nội dung tranh luận cho context."""
    profs = [f"- {p.name} ({p.role}, {p.stance[:100]})" for p in session.professors]
    
    turns_summary = []
    for turn in session.turns[-10:]:  # Last 10 turns
        turns_summary.append(f"{turn.speaker_name}: {turn.content[:200]}...")
    
    return f"""
DEBATE PARTICIPANTS:
{chr(10).join(profs)}

KEY DEBATE POINTS (last 10 turns):
{chr(10).join(turns_summary)}
"""


def _generate_paper_outline(client, topic: str, field: str, debate_summary: str) -> str:
    """Generate ICLR-style paper outline."""
    
    prompt = f"""Based on this academic debate about {field}, create an ICLR paper outline.

Topic: {topic}

{debate_summary}

Generate a structured paper outline with these sections in Vietnamese:
1. Abstract (3-4 sentences summarizing main contribution)
2. Introduction (problem statement, motivation, contribution)
3. Related Work (existing approaches and their limitations)
4. Proposed Approach/Methodology (novel aspects discussed)
5. Experimental Validation (how to validate claims)
6. Results & Analysis
7. Limitations
8. Conclusion

Format as markdown with bullet points. Be specific and research-focused."""

    def do():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": 1500, "temperature": 0.5},
        )
        return response.text.strip()
    
    result = _retry(do)
    return result or "Paper outline generation failed"


def _extract_key_findings(client, topic: str, session: DebateSession) -> list:
    """Extract key research findings từ debate."""
    
    # Gather all content
    all_content = "\n".join([
        f"{t.speaker_name}: {t.content}" 
        for t in session.turns[-15:]  # Last 15 turns
    ])
    
    prompt = f"""From this academic debate about {topic}, identify the top 5 key research findings.

Debate content:
{all_content[:2000]}

Extract findings as JSON array:
[
  {{"finding": "concise statement", "evidence": "where it came from", "impact": "why it matters"}},
  ...
]

Only return JSON array, no markdown."""

    def do():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": 800, "temperature": 0.3},
        )
        text = response.text.strip()
        text = re.sub(r"```json|```", "", text).strip()
        try:
            return json.loads(text)
        except:
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    return []
    
    result = _retry(do)
    return result if result else []


def _generate_open_questions(client, topic: str, field: str, debate_summary: str) -> list:
    """Generate open research questions for future work."""
    
    prompt = f"""Based on this debate in {field}, what are the top open research questions?

Topic: {topic}

{debate_summary}

Generate 5-7 specific, actionable research questions in Vietnamese that:
- Extend the debate
- Address mentioned limitations
- Suggest new research directions

Format as JSON array of strings:
["Question 1?", "Question 2?", ...]

Only return JSON array."""

    def do():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": 600, "temperature": 0.6},
        )
        text = response.text.strip()
        text = re.sub(r"```json|```", "", text).strip()
        try:
            return json.loads(text)
        except:
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    return []
    
    result = _retry(do)
    return result if result else []


def _generate_recommendations(client, topic: str, field: str, findings: list) -> list:
    """Generate specific recommendations for next steps."""
    
    findings_str = json.dumps(findings[:3], ensure_ascii=False)
    
    prompt = f"""Based on these research findings, suggest concrete next steps for PhD research.

Topic: {topic}
Field: {field}

Key findings:
{findings_str}

Suggest {min(config.RESEARCH_MAX_RECOMMENDATIONS, 5)} concrete recommendations in Vietnamese:
1. Type your recommendation
2. Type your recommendation
...

Each should be specific, actionable, and ICLR-relevant."""

    def do():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": 800, "temperature": 0.4},
        )
        text = response.text.strip()
        
        # Parse numbered list
        lines = text.split('\n')
        recommendations = []
        for line in lines:
            line = line.strip()
            if line and len(line) > 10:
                # Remove numbering
                cleaned = re.sub(r'^\d+\.\s*', '', line)
                if cleaned and not cleaned.startswith('['):
                    recommendations.append(cleaned)
        
        return recommendations[:config.RESEARCH_MAX_RECOMMENDATIONS]
    
    result = _retry(do)
    return result if result else []
