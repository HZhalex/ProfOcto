import os

_DIR = os.path.dirname(__file__)

def _load_from_path(path: str, **kwargs) -> str:
    """Internal: Load prompt from file path and fill placeholders."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")
    with open(path, encoding="utf-8") as f:
        template = f.read()
    return template.format_map(kwargs) if kwargs else template


def load_system(template_name: str, **kwargs) -> str:
    """Load system prompts (professor, moderator, fact_checker).
    
    Example:
        load_system("professor", name="Dr. Smith", university="MIT", ...)
        load_system("moderator")
        load_system("fact_checker")
    """
    path = os.path.join(_DIR, "system", f"{template_name}.txt")
    return _load_from_path(path, **kwargs)


def load_template(template_name: str, **kwargs) -> str:
    """Load reusable prompt templates (opening, turn_format, summary, research_kit).
    
    Example:
        load_template("opening", topic="...", participants="...")
        load_template("summary", debate_content="...")
    """
    path = os.path.join(_DIR, "templates", f"{template_name}.txt")
    return _load_from_path(path, **kwargs)


def load_research(template_name: str, **kwargs) -> str:
    """Load research synthesis prompts (paper_outline, key_findings, open_questions, recommendations).
    
    Example:
        load_research("paper_outline", topic="...", field="...", debate_summary="...")
        load_research("key_findings", topic="...", debate_content="...")
    """
    path = os.path.join(_DIR, "research", f"{template_name}.txt")
    return _load_from_path(path, **kwargs)


# Legacy compatibility - keep old load() for backward compatibility
def load(template_name: str, **kwargs) -> str:
    """Load a prompt from a .txt file and fill {key} placeholders.

    DEPRECATED: Use load_system(), load_template(), or load_research() instead.
    This function tries to find prompts in the old flat structure.
    """
    # Try to load from new structure first
    for loader in [load_system, load_template, load_research]:
        try:
            return loader(template_name, **kwargs)
        except FileNotFoundError:
            continue
    
    raise FileNotFoundError(f"Prompt not found: {template_name}")