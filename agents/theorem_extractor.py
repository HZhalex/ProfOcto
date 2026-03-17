"""
Theorem & Mathematical Foundation Extractor

Trích xuất:
- Theorems/Lemmas được cite
- Mathematical statements, proofs, assumptions
- Citations liên quan

WITH COMPREHENSIVE LOGGING FOR DEBUG
"""

import json
from typing import Dict, Any
import config
from utils.logger import get_logger


def _call_gemini_extract(prompt: str, max_tokens: int = 2000) -> str:
    """Call Gemini để extract theorems with error handling."""
    logger = get_logger()
    
    try:
        from google import genai
    except ImportError:
        logger.log_error("theorem_extractor", ImportError("google-genai not installed"))
        return "{}"
    
    logger.log_api_call("theorem_extractor", config.MODEL, len(prompt))
    
    try:
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": max_tokens, "temperature": 0.3},
        )
        result = response.text.strip()
        logger.log_api_response("theorem_extractor", len(result))
        return result
    except Exception as e:
        logger.log_error("theorem_extractor", e, context="API call failed during theorem extraction")
        return "{}"


def extract_theorems(content: str, speaker_name: str) -> Dict[str, Any]:
    """Extract mathematical foundations from professor's turn."""
    logger = get_logger()
    logger.log_theorem_extraction_start(speaker_name, len(content))
    
    try:
        extraction_prompt = f"""
Bạn là một mathematician chuyên phân tích AI papers. Analyze turn này từ professor {speaker_name}:

TURN CONTENT:
{content}

Task: Extract tất cả mathematical foundations. Respond ONLY as JSON (no markdown).

{{
    "theorems": [
        {{
            "name": "Theorem name",
            "statement": "Complete mathematical statement",
            "cite": "[Author Year]",
            "complexity": "Time/Space complexity",
            "conditions": ["Assumption 1"],
            "type": "architecture|optimization|complexity"
        }}
    ],
    "mathematical_statements": [
        {{"formula": "Math formula", "meaning": "What it represents", "cite": "[source]"}}
    ],
    "assumptions": [
        {{"assumption": "Assumption text", "context": "Where", "critical": true}}
    ],
    "proofs_or_sketch": [
        {{"claim": "What is claimed", "proof_sketch": "Why it's true"}}
    ],
    "math_density": 0.5,
    "rigor_level": "informal|moderate|rigorous|highly_rigorous"
}}
"""
        
        result_json = _call_gemini_extract(extraction_prompt, max_tokens=1500)
        
        try:
            result = json.loads(result_json)
        except json.JSONDecodeError:
            logger.log_warning("theorem_extractor", f"Invalid JSON for {speaker_name}, using defaults")
            result = {
                "theorems": [],
                "mathematical_statements": [],
                "assumptions": [],
                "proofs_or_sketch": [],
                "math_density": 0.0,
                "rigor_level": "informal"
            }
        
        result["speaker"] = speaker_name
        
        logger.log_theorem_extraction_result(
            speaker_name,
            len(result.get("theorems", [])),
            len(result.get("mathematical_statements", [])),
            len(result.get("assumptions", [])),
            len(result.get("proofs_or_sketch", [])),
            result.get("math_density", 0.0)
        )
        
        return result
    
    except Exception as e:
        logger.log_theorem_extraction_error(speaker_name, e)
        return {
            "speaker": speaker_name,
            "theorems": [],
            "mathematical_statements": [],
            "assumptions": [],
            "proofs_or_sketch": [],
            "math_density": 0.0,
            "rigor_level": "informal"
        }


def extract_citations(content: str) -> list[Dict[str, str]]:
    """Extract citations with logging."""
    logger = get_logger()
    logger.theorem_logger.debug(f"Extracting citations from content ({len(content)} chars)")
    
    try:
        import re
        
        patterns = [
            r'\[([A-Z][a-z]+(?:\s+et\s+al\.)?)\s+(\d{4})\]',
            r'\(([A-Z][a-z]+(?:\s+et\s+al\.)?),\s*(\d{4})\)',
            r'([A-Z][a-z]+(?:\s+et\s+al\.)?)\s+\((\d{4})\)',
        ]
        
        citations = []
        seen = set()
        
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                author = match.group(1)
                year = match.group(2)
                key = f"{author}_{year}"
                if key not in seen:
                    citations.append({
                        "authors": author,
                        "year": year,
                        "cite_key": key,
                        "context": content[max(0, match.start()-50):match.end()+50]
                    })
                    seen.add(key)
        
        logger.theorem_logger.debug(f"Found {len(citations)} citations")
        return citations
    
    except Exception as e:
        logger.log_error("theorem_extractor", e, context="Citation extraction failed")
        return []


def analyze_mathematical_consistency(theorems_1: Dict[str, Any], theorems_2: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze consistency between two professors' claims."""
    logger = get_logger()
    
    try:
        from google import genai
    except ImportError:
        return {"contradictions": [], "complementary_approaches": [], "unresolved_questions": []}
    
    logger.theorem_logger.debug(f"Analyzing consistency between {theorems_1.get('speaker')} and {theorems_2.get('speaker')}")
    
    try:
        consistency_prompt = f"""
Compare mathematical claims:

PROFESSOR 1 ({theorems_1.get('speaker', 'Unknown')}):
{json.dumps(theorems_1, ensure_ascii=False, indent=2)}

PROFESSOR 2 ({theorems_2.get('speaker', 'Unknown')}):
{json.dumps(theorems_2, ensure_ascii=False, indent=2)}

Detect contradictions & gaps. Respond as JSON only.

{{
    "contradictions": [
        {{"prof1_claim": "...", "prof2_claim": "...", "nature": "type", "research_gap": "..."}}
    ],
    "complementary_approaches": [],
    "unresolved_questions": []
}}
"""
        
        logger.log_api_call("consistency_analysis", config.MODEL, len(consistency_prompt))
        
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=config.MODEL,
            contents=consistency_prompt,
            config={"max_output_tokens": 1200, "temperature": 0.4},
        )
        
        result_json = response.text.strip()
        logger.log_api_response("consistency_analysis", len(result_json))
        
        try:
            return json.loads(result_json)
        except json.JSONDecodeError:
            logger.log_warning("theorem_extractor", "Invalid JSON in consistency analysis")
            return {"contradictions": [], "complementary_approaches": [], "unresolved_questions": []}
    
    except Exception as e:
        logger.log_error("theorem_extractor", e, context="Consistency analysis failed")
        return {"contradictions": [], "complementary_approaches": [], "unresolved_questions": []}
