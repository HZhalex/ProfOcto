# Prompt Structure - Option A

## Directory Organization

```
prompts/
├── __init__.py              # Load functions (load_system, load_template, load_research)
│
├── system/                  # 🎯 System prompts - defines AI behavior
│   ├── professor.txt        # Professor behavior in debate
│   ├── moderator.txt        # Moderator behavior
│   └── fact_checker.txt     # Fact-checking rules
│
├── templates/              # 📝 Reusable prompt templates
│   ├── opening.txt          # Generate opening question
│   ├── turn_format.txt      # Format for professor turns
│   ├── summary.txt          # Moderator summary template
│   └── research_kit.txt     # Research synthesis framework
│
└── research/               # 🔬 Research synthesis prompts
    ├── paper_outline.txt    # ICLR paper structure
    ├── key_findings.txt     # Extract key findings
    ├── open_questions.txt   # Generate open questions
    └── recommendations.txt  # Suggest next steps
```

## How to Load Prompts

### System Prompts

```python
from prompts import load_system

# Professor
system = load_system("professor",
    name=prof.name,
    university=prof.university,
    expertise=prof.expertise,
    personality=prof.personality,
    stance=prof.stance,
    professors_summary=session.get_professors_summary()
)

# Moderator
moderator_system = load_system("moderator")

# Fact-checker
fact_checker_system = load_system("fact_checker")
```

### Reusable Templates

```python
from prompts import load_template

# Opening question
opening = load_template("opening", topic=topic, participants=participants)

# Turn format
turn_prompt = load_template("turn_format",
    system=system_prompt,
    topic=topic,
    recent_history=history,
    speaker_name=speaker_name
)

# Summary
summary = load_template("summary", debate_content=content)

# Research kit meta-template
kit_template = load_template("research_kit",
    topic=topic,
    field=field,
    debate_summary=summary
)
```

### Research Synthesis

```python
from prompts import load_research

# Paper outline
outline = load_research("paper_outline",
    topic=topic,
    field=field,
    debate_summary=summary
)

# Key findings
findings = load_research("key_findings",
    topic=topic,
    debate_content=content
)

# Open questions
questions = load_research("open_questions",
    topic=topic,
    field=field,
    debate_summary=summary
)

# Recommendations
recommendations = load_research("recommendations",
    topic=topic,
    field=field,
    findings=findings,
    num_recommendations=5
)
```

## Benefits of This Structure

✅ **Organization** - Clear separation of concerns
✅ **Maintainability** - Easy to find and edit prompts
✅ **Scalability** - Add new prompts without cluttering
✅ **Reusability** - Templates can be used in multiple places
✅ **Flexibility** - Can easily swap implementations

## Migration Notes

### Old Code (deprecated but still works)

```python
from prompts import load
system = load("professor_base", name=prof.name, ...)
```

### New Code (recommended)

```python
from prompts import load_system
system = load_system("professor", name=prof.name, ...)
```

The `load()` function is still available for backward compatibility, but use specific loaders (`load_system`, `load_template`, `load_research`) going forward.

## File Editing Tips

1. **Tweaking debate quality?** → Edit `system/professor.txt` or `system/moderator.txt`
2. **Improving research output?** → Edit files in `research/` folder
3. **Adding new features?** → Create new file in appropriate folder + update `__init__.py`
4. **Testing prompt variations?** → Create temp files in templates/

## Future Enhancements

- [ ] Prompt versioning (system/professor_v1.txt, v2.txt, etc.)
- [ ] Prompt testing suite to validate outputs
- [ ] Dynamic prompt selection based on debate topic
- [ ] Prompt analytics to track which work best
- [ ] Multi-language support (vi, en, etc.)
