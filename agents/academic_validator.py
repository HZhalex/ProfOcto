"""
Academic Validator - Extract foundational papers, verify mathematical claims, track citations
For rigorous research AI assistant with mathematical backing
"""
import json
import re
from debate.session import DebateSession
import config


def _retry(fn, max_retries: int = 2):
    """Retry with minimal delays."""
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            if attempt < max_retries - 1:
                import time
                time.sleep(0.5)
            else:
                return None


def extract_foundational_papers(client, topic: str, field: str, debate_summary: str = "") -> dict:
    """
    Extract foundational papers for the domain.
    Identifies: core papers, key milestones, essential citations for the field.
    """
    prompt = f"""Given the research area: {field}
Topic of study: {topic}

{debate_summary}

Identify the FOUNDATIONAL PAPERS that built this field. For each paper:
1. Title and authors
2. Year published
3. Core contribution (what it introduced)
4. Key theorems/frameworks it established
5. Why it's foundational (milestone/core concept/widely cited)
6. Relevance to current topic

Return as JSON:
{{
  "field_title": "Full name of the field",
  "research_directions": ["Direction 1", "Direction 2", ...],
  "foundational_papers": [
    {{
      "title": "Paper title",
      "authors": "Author1, Author2",
      "year": 2020,
      "contribution": "What it introduced",
      "theorem_or_framework": "Mathematical/conceptual contribution",
      "significance": "Why foundational",
      "relevance_to_topic": "How it relates to current topic"
    }},
    ...
  ],
  "core_theorems": [
    {{
      "name": "Theorem/concept name",
      "paper": "Which foundational paper introduced this",
      "statement": "Mathematical statement or description",
      "implications": "What it implies for the field"
    }},
    ...
  ]
}}"""

    def call_api():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"temperature": 0.3, "max_output_tokens": 800}
        )
        text = response.text
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            return json.loads(json_match.group())
        return {"field_title": field, "foundational_papers": [], "core_theorems": []}
    
    result = _retry(call_api)
    return result or {"field_title": field, "foundational_papers": [], "core_theorems": []}


def verify_mathematical_claims(client, claims: list, field: str, foundational_papers: dict) -> dict:
    """
    Verify that claims have mathematical backing.
    Each claim must cite: theorem, bound, proof, or paper.
    """
    if not claims:
        return {"valid_claims": [], "unverified_claims": [], "suggestions": []}
    
    claims_str = json.dumps(claims[:5], ensure_ascii=False)
    papers_str = json.dumps(foundational_papers.get("foundational_papers", [])[:5], ensure_ascii=False)
    
    prompt = f"""You are a mathematical rigor validator for research in: {field}

Claims made in the debate:
{claims_str}

Foundational papers available:
{papers_str}

For each claim, assess:
1. Does it have mathematical backing? (theorem, proof, bound, formula)
2. Which paper supports it?
3. What assumptions does it rely on?
4. Are there boundary conditions or limitations?

Categorize as:
- MATHEMATICALLY_BACKED: Has clear theorem/proof/bounds backing
- NEEDS_PROOF: Makes sense but missing mathematical foundation
- UNSUPPORTED: No clear mathematical basis
- CONTRADICTS: Conflicts with established theorem

Return JSON:
{{
  "valid_claims": [
    {{
      "claim": "The claim",
      "backing": "Theorem/Bound/Proof used",
      "paper": "Which paper supports it",
      "mathematical_statement": "The actual formula/theorem",
      "assumptions": ["Assumption 1", ...]
    }},
    ...
  ],
  "unverified_claims": [
    {{
      "claim": "The claim",
      "why_unverified": "What's missing",
      "suggested_backing": "How to verify it"
    }},
    ...
  ],
  "missing_theorems": [
    "Which theorems would strengthen claims"
  ]
}}"""

    def call_api():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"temperature": 0.2, "max_output_tokens": 700}
        )
        text = response.text
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            return json.loads(json_match.group())
        return {"valid_claims": [], "unverified_claims": []}
    
    result = _retry(call_api)
    return result or {"valid_claims": [], "unverified_claims": []}


def track_citations(client, session: DebateSession, field: str, foundational_papers: dict) -> dict:
    """
    Track which foundational papers are cited by each professor.
    Build citation network and argument chains.
    """
    # Extract all turns from session (skip moderator)
    turns_data = []
    for turn in session.turns:
        if not turn.is_moderator:  # Only include professor turns
            turns_data.append({
                "professor": turn.speaker_name,
                "content": turn.content[:500] if turn.content else "",  # First 500 chars
                "turn": turn.turn_number
            })
    
    if not turns_data:
        return {"citation_map": {}, "argument_chains": []}
    
    turns_str = json.dumps(turns_data[:10], ensure_ascii=False)
    papers_list = [
        f"{p.get('title', '')} ({p.get('year', '')})" 
        for p in foundational_papers.get("foundational_papers", [])[:8]
    ]
    
    prompt = f"""Analyze citations in this debate about {field}

Foundational papers in this field:
{json.dumps(papers_list, ensure_ascii=False)}

Debate turns by professors:
{turns_str}

Track:
1. Which papers does each professor reference (explicitly or conceptually)?
2. Which theorems/frameworks from foundational papers are being used?
3. How do arguments build on each other?
4. Are claims properly grounded in the cited papers?

Return JSON:
{{
  "citation_map": {{
    "professor_name": [
      {{
        "paper": "Paper title (year)",
        "mentions": "How many times referenced",
        "usage": "How it's being used in argument"
      }},
      ...
    ]
  }},
  "argument_chains": [
    {{
      "thesis": "The main argument",
      "supporting_claims": [
        {{
          "claim": "Sub-claim",
          "paper_backing": "Which paper supports this",
          "theorem_used": "Which theorem/framework"
        }},
        ...
      ]
    }},
    ...
  ],
  "gaps_in_citation": [
    "Arguments that lack mathematical backing"
  ]
}}"""

    def call_api():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"temperature": 0.2, "max_output_tokens": 700}
        )
        text = response.text
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            return json.loads(json_match.group())
        return {"citation_map": {}, "argument_chains": []}
    
    result = _retry(call_api)
    return result or {"citation_map": {}, "argument_chains": []}


def validate_debate_rigor(client, session: DebateSession, topic: str, field: str) -> dict:
    """
    Validate if debate achieved academic rigor standards.
    Check: use of foundational papers, mathematical backing, proper assumptions.
    """
    turns_count = len(session.turns)
    summary = _build_debate_summary_simple(session)
    
    prompt = f"""Assess the academic rigor of this debate on {topic} in field {field}

Debate summary (first 800 chars):
{summary[:800]}

Number of turns: {turns_count}

Evaluate:
1. Do professors cite specific papers?
2. Are mathematical theorems explicitly stated?
3. Are assumptions clearly defined?
4. Do counterarguments address actual mathematical issues (not just opinions)?
5. Are bounds, complexity, or convergence properties discussed?
6. Is the debate grounded in established mathematical frameworks?

Rate on scale 1-10 and provide feedback.

Return JSON:
{{
  "rigor_score": 7,
  "strengths": ["What was done well"],
  "weaknesses": ["What needs improvement"],
  "missing_elements": ["What should have been discussed"],
  "recommendation": "Specific ways to improve rigor",
  "is_phd_level": true,
  "next_steps_for_dissertation": "How to deepen for dissertation work"
}}"""

    def call_api():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"temperature": 0.2, "max_output_tokens": 600}
        )
        text = response.text
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            return json.loads(json_match.group())
        return {
            "rigor_score": 0,
            "strengths": [],
            "weaknesses": [],
            "missing_elements": [],
            "recommendation": ""
        }
    
    result = _retry(call_api)
    return result or {"rigor_score": 0, "strengths": [], "weaknesses": []}


def _build_debate_summary_simple(session: DebateSession) -> str:
    """Simple summary of debate for validation."""
    summary = ""
    for turn in session.turns[:10]:  # First 10 turns
        if not turn.is_moderator:  # Skip moderator turns
            summary += f"\n{turn.speaker_name}: {turn.content[:300]}"
    return summary


def validate_evidence_strength(client, claims: list, foundational_papers: dict) -> dict:
    """
    Validate that claims have SUFFICIENT evidence (3-5+ papers, diverse sources).
    Every major claim must have multiple papers backing it, not just one.
    """
    if not claims:
        return {"strong_claims": [], "weak_claims": [], "evidence_gaps": []}
    
    claims_str = json.dumps(claims[:5], ensure_ascii=False)
    papers_list = [
        f"{p.get('title', '')[:60]} ({p.get('authors', '')[:30]}, {p.get('year', '')})" 
        for p in foundational_papers.get("foundational_papers", [])[:10]
    ]
    
    prompt = f"""Assess EVIDENCE STRENGTH for these claims in academic research.

Claims made:
{claims_str}

Available foundational papers:
{json.dumps(papers_list, ensure_ascii=False)}

For EACH claim, determine:
1. How many papers currently back it? (should be 3-5+ for major claims)
2. Are they from diverse sources/groups? (same group's papers don't count as diversity)
3. Does it have theoretical + empirical + proof backing?
4. What type of claim is it? (theoretical/methodological/empirical)

STANDARDS:
- THEORETICAL claim (needs 4-5 papers): proof, related work, empirical validation, alternative approaches
- METHODOLOGICAL claim (needs 3-4 papers): method paper, theoretical proof, independent validation, comparison
- EMPIRICAL claim (needs 2-3 papers): your results, baselines, independent verification

Return JSON:
{{
  "strong_claims": [
    {{
      "claim": "The claim",
      "evidence_count": 5,
      "papers_cited": ["Paper1 (Year)", "Paper2 (Year)", ...],
      "diversity": "diverse sources or same group",
      "strength": "very strong / strong / adequate",
      "reasoning": "Why evidence is sufficient"
    }},
    ...
  ],
  "weak_claims": [
    {{
      "claim": "The claim",
      "evidence_count": 1,
      "papers_cited": ["Paper1 (Year)"],
      "why_weak": "Only 1 paper, needs 3-5 for major claim",
      "how_to_strengthen": "Add papers from [sources], include [type of evidence]",
      "claim_type": "theoretical / methodological / empirical"
    }},
    ...
  ],
  "evidence_gaps": [
    "What types of papers/evidence are completely missing"
  ],
  "overall_evidence_score": 6.5
}}"""

    def call_api():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"temperature": 0.2, "max_output_tokens": 700}
        )
        text = response.text
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            return json.loads(json_match.group())
        return {"strong_claims": [], "weak_claims": [], "evidence_gaps": []}
    
    result = _retry(call_api)
    return result or {"strong_claims": [], "weak_claims": [], "evidence_gaps": []}


def validate_gap_foundation_solution(client, session: DebateSession, topic: str, field: str) -> dict:
    """
    Validate that arguments follow Gap-Foundation-Solution-RemainingGap structure.
    Each major claim should:
    1. Identify a research gap
    2. State mathematical foundation
    3. Propose solution with theorem backing
    4. Acknowledge remaining gaps
    """
    summary = _build_debate_summary_simple(session)
    
    prompt = f"""Analyze if arguments in this debate follow STRONG academic structure:
Topic: {topic}
Field: {field}

Debate summary (first 800 chars):
{summary[:800]}

Check each argument for this 4-part structure:

1. RESEARCH GAP - What problem is unsolved?
2. MATHEMATICAL FOUNDATION - What theorem reveals this gap?
3. SOLUTION - How does proposed approach address it?
4. REMAINING GAP - What's still unsolved?

Example of STRONG argument:
"Gap: ReLU networks have spectral bias (Rahaman et al., 2019).
Foundation: By spectral bias theorem, learning frequency Ï‰ requires O(Ï‰Â²/Îµ) samples.
Solution: Fourier positional encoding (Tancik et al., 2020) explicitly covers frequencies [2â°, 2^L].
Remaining: Only works for band-limited functions; natural images need learnable activations."

Example of WEAK argument:
"Fourier features are better than ReLU because Tancik et al. showed it works."
[Missing: explicit gap, foundation, remaining limitations]

Return JSON:
{{
  "strong_arguments": [
    {{
      "argument": "Summary of argument",
      "gap_identified": "specific research gap stated",
      "mathematical_foundation": "theorem or principle",
      "solution_proposed": "method that addresses gap",
      "remaining_gap_acknowledged": "limitations stated",
      "completeness": "complete / partial / weak"
    }},
    ...
  ],
  "weak_arguments": [
    {{
      "argument": "Summary",
      "missing_element": "gap / foundation / solution / remaining gap",
      "suggestion": "How to strengthen"
    }},
    ...
  ],
  "gap_foundation_solution_score": 7.0,
  "overall_assessment": "Well-structured research debate or needs improvement"
}}"""

    def call_api():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"temperature": 0.2, "max_output_tokens": 700}
        )
        text = response.text
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            return json.loads(json_match.group())
        return {
            "strong_arguments": [],
            "weak_arguments": [],
            "gap_foundation_solution_score": 0,
            "overall_assessment": ""
        }
    
    result = _retry(call_api)
    return result or {
        "strong_arguments": [],
        "weak_arguments": [],
        "gap_foundation_solution_score": 0
    }


def calculate_claim_evidence_score(claim: str, papers_cited: list) -> dict:
    """
    Calculate evidence strength score for a single claim (0-10 scale).
    Based on: number of papers, diversity, types of evidence.
    """
    score = 0.0
    details = []
    
    # Base: number of papers
    if len(papers_cited) >= 5:
        score += 4.0
        details.append("âœ“ 5+ papers cited")
    elif len(papers_cited) >= 4:
        score += 3.5
        details.append("âœ“ 4 papers cited")
    elif len(papers_cited) >= 3:
        score += 2.5
        details.append("âš  3 papers (minimum for major claim)")
    elif len(papers_cited) >= 2:
        score += 1.5
        details.append("âš  2 papers (inadequate)")
    elif len(papers_cited) >= 1:
        score += 0.5
        details.append("âœ— 1 paper only")
    
    # Diversity bonus: different authors/years
    authors = set()
    years = set()
    for paper in papers_cited:
        # Extract author and year from "Title (Author, Year)" format
        match = re.search(r'\(([^,]+),\s*(\d+)\)', paper)
        if match:
            authors.add(match.group(1).strip())
            years.add(match.group(2))
    
    if len(authors) >= len(papers_cited) * 0.7:  # At least 70% different authors
        score += 2.0
        details.append("âœ“ Diverse sources (different authors)")
    else:
        details.append("âš  Limited source diversity")
    
    if len(years) >= 2:  # Papers from multiple eras strengthen claims
        score += 1.5
        details.append("âœ“ Multiple time periods")
    
    # Evidence type bonus (if mentions proof, theorems, experimental data)
    # This would need to be extracted from actual claim text
    
    # Cap at 10
    score = min(score, 10.0)
    
    # Assessment
    if score >= 8.5:
        assessment = "Excellent - strong evidence"
    elif score >= 7.0:
        assessment = "Good - adequate evidence"
    elif score >= 5.0:
        assessment = "Adequate - needs strengthening"
    elif score >= 3.0:
        assessment = "Weak - insufficient evidence"
    else:
        assessment = "Very Weak - major evidence gap"
    
    return {
        "score": round(score, 1),
        "assessment": assessment,
        "paper_count": len(papers_cited),
        "unique_authors": len(authors),
        "year_range": f"{min(years)}-{max(years)}" if years else "N/A",
        "details": details
    }

