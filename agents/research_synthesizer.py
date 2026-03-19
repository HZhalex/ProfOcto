"""
Research Synthesizer - Generate research kit từ debate sessions
Tạo paper outline, key findings, citations, và open questions
"""
import json
import re
from debate.session import DebateSession
import config
from agents import academic_validator


def _retry(fn, max_retries: int = 2):
    """Retry with minimal delays."""
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:  # Broad exception for API errors
            if attempt < max_retries - 1:
                import time
                time.sleep(0.5)  # Short fixed delay
            else:
                return None


def generate_research_kit(session: DebateSession, topic: str, field: str) -> dict:
    """
    Generate comprehensive research kit từ debate session.
    Includes: outline, findings, gaps, novel approaches, theoretical foundations, breakthrough areas.
    Designed for PhD-level research with academic rigor.
    """
    if not config.RESEARCH_MODE:
        return {}

    print(f"[Research] Synthesizing research kit for: {topic[:60]}", flush=True)
    
    try:
        from google import genai
    except ImportError:
        print("[Research] google-genai not installed, skipping research kit generation")
        return {}
    
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    
    # 1. Summarize debate for context
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
    
    # 6. NEW: Analyze research gaps in detail
    print("[Research] Analyzing research gaps...", flush=True)
    research_gaps = _analyze_research_gaps(client, topic, field, findings, debate_summary)
    
    # 7. NEW: Identify novel approaches discussed
    print("[Research] Identifying novel approaches...", flush=True)
    novel_approaches = _extract_novel_approaches(client, topic, session)
    
    # 8. NEW: Identify theoretical foundations
    print("[Research] Mapping theoretical foundations...", flush=True)
    theoretical_foundations = _extract_theoretical_foundations(client, topic, field, debate_summary)
    
    # 9. NEW: Identify potential breakthroughs
    print("[Research] Identifying breakthrough potential...", flush=True)
    breakthrough_areas = _identify_breakthrough_areas(client, topic, field, findings, novel_approaches)
    
    # 10. NEW: Methodology innovations
    print("[Research] Analyzing methodology innovations...", flush=True)
    methodology_innovations = _extract_methodology_innovations(client, topic, session)
    
    # 11. NEW: Cross-domain insights
    print("[Research] Extracting cross-domain insights...", flush=True)
    cross_domain = _extract_cross_domain_insights(client, topic, field, debate_summary)
    
    # 12. NEW: Counterarguments and limitations
    print("[Research] Analyzing counterarguments...", flush=True)
    counterarguments = _extract_counterarguments(client, topic, session)
    
    # 13. NEW (MATHEMATICAL): Extract mathematical frameworks and theorems
    print("[Research] Extracting mathematical frameworks...", flush=True)
    math_frameworks = _extract_mathematical_frameworks(client, topic, field, session)
    
    # 14. NEW (MATHEMATICAL): Analyze mathematical gaps and assumptions
    print("[Research] Analyzing mathematical assumptions and gaps...", flush=True)
    math_gaps = _analyze_mathematical_gaps(client, topic, session)
    
    # 15. NEW (MATHEMATICAL): Compare mathematical approaches
    print("[Research] Comparing mathematical approaches...", flush=True)
    math_comparison = _compare_mathematical_approaches(client, topic, session)
    
    # 16. NEW (ACADEMIC RIGOR): Extract foundational papers
    print("[Research] Identifying foundational papers for the field...", flush=True)
    foundational_papers = academic_validator.extract_foundational_papers(client, topic, field, debate_summary)
    
    # 17. NEW (ACADEMIC RIGOR): Verify mathematical claims
    print("[Research] Verifying mathematical claims with academic backing...", flush=True)
    verified_claims = academic_validator.verify_mathematical_claims(client, findings, field, foundational_papers)
    
    # 18. NEW (ACADEMIC RIGOR): Track citations
    print("[Research] Tracking citations and argument chains...", flush=True)
    citation_analysis = academic_validator.track_citations(client, session, field, foundational_papers)
    
    # 19. NEW (ACADEMIC RIGOR): Validate debate rigor
    print("[Research] Validating debate academic rigor...", flush=True)
    debate_rigor = academic_validator.validate_debate_rigor(client, session, topic, field)
    
    # 20. NEW (EVIDENCE STRENGTH): Validate evidence sufficiency
    print("[Research] Assessing evidence strength and diversity...", flush=True)
    evidence_strength = academic_validator.validate_evidence_strength(client, findings, foundational_papers)
    
    # 21. NEW (GAP-FOUNDATION-SOLUTION): Validate argument structure
    print("[Research] Validating Gap-Foundation-Solution structure...", flush=True)
    gfs_analysis = academic_validator.validate_gap_foundation_solution(client, session, topic, field)
    
    kit = {
        "topic": topic,
        "field": field,
        "outline": outline,
        "key_findings": findings,
        "research_gaps": research_gaps,  # NEW
        "novel_approaches": novel_approaches,  # NEW
        "theoretical_foundations": theoretical_foundations,  # NEW
        "breakthrough_areas": breakthrough_areas,  # NEW
        "methodology_innovations": methodology_innovations,  # NEW
        "cross_domain_insights": cross_domain,  # NEW
        "counterarguments": counterarguments,  # NEW
        "mathematical_frameworks": math_frameworks,  # NEW (MATH)
        "mathematical_gaps": math_gaps,  # NEW (MATH)
        "mathematical_comparison": math_comparison,  # NEW (MATH)
        "foundational_papers": foundational_papers,  # NEW (ACADEMIC RIGOR)
        "verified_claims": verified_claims,  # NEW (ACADEMIC RIGOR)
        "citation_analysis": citation_analysis,  # NEW (ACADEMIC RIGOR)
        "debate_rigor": debate_rigor,  # NEW (ACADEMIC RIGOR)
        "evidence_strength": evidence_strength,  # NEW (EVIDENCE VALIDATION)
        "gap_foundation_solution": gfs_analysis,  # NEW (ARGUMENT STRUCTURE)
        "open_questions": open_questions,
        "recommendations": recommendations,
    }
    
    print("[Research] Research kit generated successfully", flush=True)
    return kit


def _analyze_research_gaps(client, topic: str, field: str, findings: list, debate_summary: str) -> list:
    """Analyze critical research gaps and unexplored territories."""
    findings_str = json.dumps(findings[:3], ensure_ascii=False) if findings else "[]"
    
    prompt = f"""Analyze CRITICAL RESEARCH GAPS in this field regarding: {topic}

Field: {field}

Current findings from debate:
{findings_str}

{debate_summary}

Identify 5-7 specific research gaps that represent UNEXPLORED TERRITORIES:
- What nobody has studied yet
- What traditional approaches CANNOT address
- What theoretical frameworks are MISSING
- What empirical data is LACKING
- What fundamental assumptions need QUESTIONING

Return as JSON array:
[
  {{"gap": "specific gap description", "significance": "why it matters for breakthroughs", "difficulty": "theoretical/empirical/computational"}},
  ...
]

Be specific, academically rigorous, actionable for PhD research."""

    def do():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": 1000, "temperature": 0.7},
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


def _extract_novel_approaches(client, topic: str, session: DebateSession) -> list:
    """Extract NOVEL approaches and methodologies discussed in debate."""
    all_content = "\n".join([f"{t.speaker_name}: {t.content}" for t in session.turns[-15:]])
    
    prompt = f"""From this academic debate about "{topic}", identify NOVEL APPROACHES that differ from traditional methods.

Debate content:
{all_content[:2500]}

Extract the TOP NOVEL APPROACHES (new ways to think about / solve the problem):

Return JSON array:
[
  {{"approach": "concise name", "description": "how it works", "novelty": "why it's novel", "challenges": "implementation challenges"}},
  ...
]

Focus on approaches that are:
- NOT mainstream/conventional  
- Based on new principles or combinations
- Potentially paradigm-shifting
- Technically sound but underexplored

Return only JSON, no markdown."""

    def do():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": 1200, "temperature": 0.75},
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


def _extract_theoretical_foundations(client, topic: str, field: str, debate_summary: str) -> list:
    """Identify theoretical foundations and theoretical gaps."""
    prompt = f"""Analyze theoretical foundations for: {topic}

Field: {field}

Debate insights:
{debate_summary}

Identify:
1. CURRENT theoretical frameworks being used
2. THEORETICAL GAPS or inconsistencies
3. NEW theoretical frameworks that could apply
4. MATHEMATICAL/LOGICAL foundations that need strengthening
5. Links to FUNDAMENTAL PRINCIPLES in {field}

Return JSON array:
[
  {{"foundation": "name/concept", "description": "what it is", "applicability": "how relevant to {topic}", "gaps": "what's missing"}},
  ...
]

Academic rigor: HIGH. Focus on THEORETICAL DEPTH."""

    def do():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": 1000, "temperature": 0.6},
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


def _identify_breakthrough_areas(client, topic: str, field: str, findings: list, approaches: list) -> list:
    """Identify areas with MAXIMUM BREAKTHROUGH POTENTIAL."""
    findings_str = json.dumps(findings[:3], ensure_ascii=False) if findings else "[]"
    approaches_str = json.dumps(approaches[:3], ensure_ascii=False) if approaches else "[]"
    
    prompt = f"""Based on emerging ideas, identify BREAKTHROUGH AREAS with maximum innovation potential.

Topic: {topic}
Field: {field}

Key findings:
{findings_str}

Novel approaches:
{approaches_str}

Identify 4-6 BREAKTHROUGH AREAS where small advances could have DISPROPORTIONATE impact:

Return JSON array:
[
  {{"area": "specific area", "breakthrough_potential": "why this matters", "required_advances": "what's needed to break through", "timeline": "estimated time to impact", "risk_level": "high/medium/low complexity"}},
  ...
]

Think like a researcher seeking to CHANGE THE FIELD."""

    def do():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": 1000, "temperature": 0.8},
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


def _extract_methodology_innovations(client, topic: str, session: DebateSession) -> list:
    """Extract innovative methodologies and experimental designs discussed."""
    all_content = "\n".join([f"{t.speaker_name}: {t.content}" for t in session.turns[-12:]])
    
    prompt = f"""From this debate about "{topic}", identify METHODOLOGICAL INNOVATIONS.

Debate:
{all_content[:2000]}

Extract innovative METHODOLOGIES, EXPERIMENTAL DESIGNS, or VALIDATION APPROACHES discussed:

Return JSON:
[
  {{"method": "name", "description": "how it works", "novelty": "what's new/innovative", "applicability": "where it applies", "advantages": "benefits over traditional approaches"}},
  ...
]

Focus on:
- New ways to test hypotheses
- Innovative measurement techniques  
- Novel analytical frameworks
- Cross-disciplinary methodologies

Return only JSON."""

    def do():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": 900, "temperature": 0.7},
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


def _extract_cross_domain_insights(client, topic: str, field: str, debate_summary: str) -> list:
    """Extract cross-domain insights that could apply from other fields."""
    prompt = f"""What CROSS-DOMAIN INSIGHTS from other fields could revolutionize work on: {topic}?

Field: {field}

Debate context:
{debate_summary}

Think about:
- Physics/Math principles applicable here
- Biology/Neuroscience inspiration
- Computer Science techniques
- Economics/Game Theory concepts
- Operations Research methods
- Other AI/ML subfields

Identify 5-7 CROSS-DOMAIN INSIGHTS with HIGH APPLICABILITY POTENTIAL:

Return JSON:
[
  {{"source_field": "which field", "insight": "what insight", "application": "how to apply to {topic}", "novelty": "why this is new connection", "impact": "potential impact"}},
  ...
]

Be creative but academically rigorous."""

    def do():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": 1000, "temperature": 0.75},
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


def _extract_counterarguments(client, topic: str, session: DebateSession) -> dict:
    """Extract and analyze counterarguments and conflicting viewpoints."""
    profs_summary = [f"{p.name} ({p.stance[:80]})" for p in session.professors]
    all_turns = "\n\n".join([f"**{t.speaker_name}**: {t.content}" for t in session.turns[-10:]])
    
    prompt = f"""Analyze COUNTERARGUMENTS and CONFLICTING VIEWPOINTS in this debate about: {topic}

Professors and their stances:
{'; '.join(profs_summary)}

Key debate exchanges:
{all_turns[:2000]}

Analyze:
1. What are the STRONGEST counterarguments to the mainstream position?
2. What HIDDEN ASSUMPTIONS in the debate need questioning?
3. What TRADE-OFFS are not fully acknowledged?
4. What EDGE CASES challenge the proposed approaches?
5. What EMPIRICAL EVIDENCE contradicts certain claims?

Return JSON:
{{
  "counterarguments": [...],
  "hidden_assumptions": [...],
  "tradeoffs": [...],
  "edge_cases": [...],
  "empirical_challenges": [...]
}}

Where each array contains objects with "point" and "significance" fields.

Be critically rigorous."""

    def do():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": 1200, "temperature": 0.65},
        )
        text = response.text.strip()
        text = re.sub(r"```json|```", "", text).strip()
        try:
            return json.loads(text)
        except:
            return {
                "counterarguments": [],
                "hidden_assumptions": [],
                "tradeoffs": [],
                "edge_cases": [],
                "empirical_challenges": []
            }
    
    result = _retry(do)
    return result if result else {"counterarguments": [], "hidden_assumptions": [], "tradeoffs": [], "edge_cases": [], "empirical_challenges": []}


def _extract_mathematical_frameworks(client, topic: str, field: str, session: DebateSession) -> list:
    """Extract mathematical frameworks, theorems, and formal foundations discussed."""
    profs_stances = [f"{p.name}: {p.stance[:100]}" for p in session.professors]
    all_turns = "\n\n".join([f"**{t.speaker_name}**: {t.content}" for t in session.turns[-12:]])
    
    prompt = f"""From this academic debate about "{topic}", extract MATHEMATICAL FRAMEWORKS and THEOREMS.

Field: {field}
Professors' viewpoints:
{'; '.join(profs_stances)}

Key debate points:
{all_turns[:2500]}

Identify:
1. MAIN MATHEMATICAL FRAMEWORKS mentioned (e.g., Fourier analysis, differential geometry, measure theory)
2. SPECIFIC THEOREMS referenced or implied (e.g., "Approximation by Fourier series", "Lipschitz continuity")
3. MATHEMATICAL ASSUMPTIONS required (e.g., "assumes smoothness C^k", "requires compactness")
4. BOUNDS discussed (approximation error, computational complexity bounds)
5. KEY MATHEMATICAL PROPERTIES (symmetry, invariance, conservation laws)

Return JSON array:
[
  {{"framework": "name (e.g., 'Fourier Analysis')", "theorems": ["theorem 1", "theorem 2"], "assumptions": ["assumption 1"], "bounds": "approximation/complexity bounds if mentioned", "properties": "key mathematical properties"}},
  ...
]

Focus on RIGOROUS mathematical content, not vague intuitions."""

    def do():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": 1200, "temperature": 0.6},
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


def _analyze_mathematical_gaps(client, topic: str, session: DebateSession) -> dict:
    """Analyze mathematical gaps, missing proofs, and unvalidated assumptions."""
    all_turns = "\n\n".join([f"**{t.speaker_name}**: {t.content}" for t in session.turns[-10:]])
    
    prompt = f"""Analyze MATHEMATICAL GAPS and UNPROVEN ASSUMPTIONS in this debate about "{topic}".

Debate exchanges:
{all_turns[:2000]}

Identify:
1. UNPROVEN CLAIMS: Arguments that sound rigorous but lack formal proof
2. MISSING ASSUMPTIONS: What must be true for the arguments to hold? (smoothness, compactness, boundedness, etc.)
3. BOUNDARY CASES: When do the theorems/approximations BREAK? (e.g., "works for C^1 functions but not for Lipschitz")
4. COMPLEXITY GAPS: What about computational complexity? Is it discussed?
5. OPEN QUESTIONS: What mathematical problems remain unsolved?

Return JSON:
{{
  "unproven_claims": [
    {{"claim": "what was claimed", "issue": "why it lacks proof", "needed": "what theorem/lemma would validate it"}}
  ],
  "missing_assumptions": [
    {{"framework": "which approach", "assumptions": ["assumption 1", "assumption 2"], "validation": "how to check these?"}}
  ],
  "boundary_failures": [
    {{"theorem": "which result", "fails_when": "specific conditions", "counterexample": "if known"}}
  ],
  "complexity_gaps": [
    {{"approach": "which method", "time_complexity": "estimated O(?) or unknown", "space_complexity": "estimated O(?) or unknown"}}
  ],
  "open_problems": ["problem 1", "problem 2"]
}}

Be mathematically precise and critical."""

    def do():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": 1200, "temperature": 0.65},
        )
        text = response.text.strip()
        text = re.sub(r"```json|```", "", text).strip()
        try:
            return json.loads(text)
        except:
            return {
                "unproven_claims": [],
                "missing_assumptions": [],
                "boundary_failures": [],
                "complexity_gaps": [],
                "open_problems": []
            }
    
    result = _retry(do)
    return result if result else {"unproven_claims": [], "missing_assumptions": [], "boundary_failures": [], "complexity_gaps": [], "open_problems": []}


def _compare_mathematical_approaches(client, topic: str, session: DebateSession) -> list:
    """Compare different mathematical approaches: trade-offs, bounds, assumptions."""
    profs_by_stance = {}
    for p in session.professors:
        profs_by_stance[p.name] = p.stance[:150]
    
    all_turns = "\n\n".join([f"**{t.speaker_name}**: {t.content}" for t in session.turns[-10:]])
    
    prompt = f"""From this debate on "{topic}", create a MATHEMATICAL COMPARISON of different approaches.

Professors and their positions:
{json.dumps(profs_by_stance, ensure_ascii=False)}

Debate:
{all_turns[:2000]}

Create a detailed MATHEMATICAL COMPARISON including:
1. CORE MATHEMATICAL DIFFERENCE (what's fundamentally different about the approaches?)
2. APPROXIMATION BOUNDS comparison (which has better error bounds and under what conditions?)
3. COMPUTATIONAL COMPLEXITY (O(?) analysis for each approach)
4. CONVERGENCE PROPERTIES (which converges how fast? What are convergence conditions?)
5. ASSUMPTIONS REQUIRED (what must be true for each approach?)
6. TRADE-OFFS (accuracy vs speed, generality vs efficiency, etc.)

Return JSON array:
[
  {{
    "approach_name": "name/identifier",
    "key_theorem": "main theorem/foundation",
    "approximation_bound": "error bound (e.g., O(1/n) or unknown)",
    "time_complexity": "O(?) notation",
    "convergence_rate": "e.g., linear, quadratic, etc.",
    "assumptions": ["assumption 1", "assumption 2"],
    "advantages": "when/why this is best",
    "disadvantages": "when/why this fails",
    "compared_to": "which other approaches"
  }},
  ...
]

Focus on mathematical properties, not marketing."""

    def do():
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": 1400, "temperature": 0.6},
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


def save_research_kit(kit: dict, directory: str = "research_kits") -> str:
    """Save research kit to files in the specified directory."""
    import os
    import json
    
    os.makedirs(directory, exist_ok=True)
    topic_slug = kit.get("topic", "unknown")[:40].replace(" ", "_").replace("/", "-")
    base_filename = f"{directory}/research_kit_{topic_slug}"
    
    # Save outline
    outline_file = f"{base_filename}_outline.md"
    with open(outline_file, "w", encoding="utf-8") as f:
        f.write(f"# Research Paper Outline\n\n**Topic:** {kit.get('topic', '')}\n\n**Field:** {kit.get('field', '')}\n\n{kit.get('outline', '')}")
    
    # Save key findings
    findings_file = f"{base_filename}_findings.json"
    with open(findings_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("key_findings", []), f, ensure_ascii=False, indent=2)
    
    # Save open questions
    questions_file = f"{base_filename}_questions.json"
    with open(questions_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("open_questions", []), f, ensure_ascii=False, indent=2)
    
    # Save recommendations
    recommendations_file = f"{base_filename}_recommendations.json"
    with open(recommendations_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("recommendations", []), f, ensure_ascii=False, indent=2)
    
    # Save research gaps (NEW)
    gaps_file = f"{base_filename}_research_gaps.json"
    with open(gaps_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("research_gaps", []), f, ensure_ascii=False, indent=2)
    
    # Save novel approaches (NEW)
    approaches_file = f"{base_filename}_novel_approaches.json"
    with open(approaches_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("novel_approaches", []), f, ensure_ascii=False, indent=2)
    
    # Save theoretical foundations (NEW)
    theory_file = f"{base_filename}_theoretical_foundations.json"
    with open(theory_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("theoretical_foundations", []), f, ensure_ascii=False, indent=2)
    
    # Save breakthrough areas (NEW)
    breakthrough_file = f"{base_filename}_breakthrough_areas.json"
    with open(breakthrough_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("breakthrough_areas", []), f, ensure_ascii=False, indent=2)
    
    # Save methodology innovations (NEW)
    methods_file = f"{base_filename}_methodology_innovations.json"
    with open(methods_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("methodology_innovations", []), f, ensure_ascii=False, indent=2)
    
    # Save cross-domain insights (NEW)
    cross_file = f"{base_filename}_cross_domain_insights.json"
    with open(cross_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("cross_domain_insights", []), f, ensure_ascii=False, indent=2)
    
    # Save counterarguments (NEW)
    counter_file = f"{base_filename}_counterarguments.json"
    with open(counter_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("counterarguments", {}), f, ensure_ascii=False, indent=2)
    
    # Save mathematical frameworks (MATHEMATICAL ANALYSIS)
    math_frameworks_file = f"{base_filename}_mathematical_frameworks.json"
    with open(math_frameworks_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("mathematical_frameworks", []), f, ensure_ascii=False, indent=2)
    
    # Save mathematical gaps (MATHEMATICAL ANALYSIS)
    math_gaps_file = f"{base_filename}_mathematical_gaps.json"
    with open(math_gaps_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("mathematical_gaps", {}), f, ensure_ascii=False, indent=2)
    
    # Save mathematical approach comparison (MATHEMATICAL ANALYSIS)
    math_comparison_file = f"{base_filename}_mathematical_comparison.json"
    with open(math_comparison_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("mathematical_comparison", []), f, ensure_ascii=False, indent=2)
    
    # Save foundational papers (ACADEMIC RIGOR)
    papers_file = f"{base_filename}_foundational_papers.json"
    with open(papers_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("foundational_papers", {}), f, ensure_ascii=False, indent=2)
    
    # Save verified claims (ACADEMIC RIGOR)
    claims_file = f"{base_filename}_verified_claims.json"
    with open(claims_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("verified_claims", {}), f, ensure_ascii=False, indent=2)
    
    # Save citation analysis (ACADEMIC RIGOR)
    citations_file = f"{base_filename}_citation_analysis.json"
    with open(citations_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("citation_analysis", {}), f, ensure_ascii=False, indent=2)
    
    # Save debate rigor assessment (ACADEMIC RIGOR)
    rigor_file = f"{base_filename}_debate_rigor.json"
    with open(rigor_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("debate_rigor", {}), f, ensure_ascii=False, indent=2)
    
    # Save evidence strength assessment (EVIDENCE VALIDATION)
    evidence_file = f"{base_filename}_evidence_strength.json"
    with open(evidence_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("evidence_strength", {}), f, ensure_ascii=False, indent=2)
    
    # Save Gap-Foundation-Solution analysis (ARGUMENT STRUCTURE)
    gfs_file = f"{base_filename}_gap_foundation_solution.json"
    with open(gfs_file, "w", encoding="utf-8") as f:
        json.dump(kit.get("gap_foundation_solution", {}), f, ensure_ascii=False, indent=2)
    
    # Save complete kit as JSON (comprehensive, all sections)
    kit_file = f"{base_filename}_complete.json"
    with open(kit_file, "w", encoding="utf-8") as f:
        json.dump(kit, f, ensure_ascii=False, indent=2)
    
    return kit_file


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

Generate a structured paper outline with these sections in English:
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
            config={"max_output_tokens": 800, "temperature": 0.5},
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

Generate 5-7 specific, actionable research questions in English that:
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

Suggest {min(config.RESEARCH_MAX_RECOMMENDATIONS, 5)} concrete recommendations in English:
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
