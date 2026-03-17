# Vietnamese Language Enforcement - Update

## Problem

Professors were sometimes responding in English instead of Vietnamese, even though prompts requested Vietnamese.

## Solution Implemented

### 1. **Strengthened Prompts**

- Moved Vietnamese requirement to the TOP of professor system prompt (before all other instructions)
- Made it CRITICAL and emphatic
- Repeated the requirement multiple times in different languages
- File changes:
  - `prompts/system/professor.txt` - Added bold warning at top
  - `prompts/system/moderator.txt` - Strengthened Vietnamese requirement
  - `prompts/templates/turn_format.txt` - Added Vietnamese requirement reminder

### 2. **Language Detection & Retry Logic**

Added to `agents/professor.py`:

```python
def _is_primarily_english(text: str) -> bool:
    """Intelligently detect if response is primarily English.

    Uses:
    - Common English word dictionary (the, is, and, model, training, etc.)
    - English word ratio threshold (>35%)
    - English word sequence detection (3+ consecutive English words)
    """

def generate_professor_turn(prof, session, stream_callback):
    # Try generating up to 2 times
    # If response detected as English -> regenerate with stronger instruction
    # Lower temperature on retry for more focused response
    # Return first non-English response
```

### 3. **How It Works**

**First attempt:**

```python
system_prompt + topic + debate_history + "Respond now in Vietnamese only."
temperature = 0.7
```

**If detected as English, retry:**

```python
system_prompt + topic + debate_history +
"*** CRITICAL: Your previous response was in English.
You MUST respond ENTIRELY in Vietnamese this time. Không tiếng Anh!! ***"
temperature = 0.5  # Lower for more controlled response
```

### 4. **Language Detection Algorithm**

The `_is_primarily_english()` function:

1. Extracts all English-like words (a-z)
2. Checks against common English words (~60 words)
3. Calculates English word ratio
4. Detects consecutive English word sequences
5. **Returns True if:**
   - > 35% of words are common English words, OR
   - Has English word sequences AND >25% English words

This catches:

- ✅ Fully English responses
- ✅ Mixed English-Vietnamese (especially if English is prominent)
- ✅ Technical English mixed with Vietnamese

Preserves Vietnamese:

- ✅ Vietnamese with technical terms (model, data, etc.)
- ✅ Vietnamese with occasional English word transliteration
- ✅ Proper academic Vietnamese

### 5. **Logging**

New logs to track language enforcement:

- `[Lang Check] Detection result: English` - Detected English response
- `[Lang Check] Retrying with stronger instruction...` - Regenerating
- `[Lang Check] WARNING: Still English after retry` - Failed both attempts (rare)

## Testing

The language detection was tested with:

- Pure Vietnamese text → Correctly identified as Vietnamese
- Pure English text → Correctly identified as English
- Mixed text → Correctly warns about English
- Vietnamese with technical terms → Correctly identified as Vietnamese

## Configuration

In `config.py`:

```python
# Can add future flag to disable retry if needed
ENFORCE_VIETNAMESE = True  # Should be added for flexibility
```

## Next Steps

1. Test debate - should now get Vietnamese responses
2. If still getting English: Check backend logs for language detection results
3. Can adjust threshold (>0.35) if too strict/lenient
4. Can add more English words to dictionary if missing patterns

## Files Modified

- `prompts/system/professor.txt`
- `prompts/system/moderator.txt`
- `prompts/templates/turn_format.txt`
- `agents/professor.py` (added language detection + retry logic)

## Performance Impact

- **Minimal**: Only regens if English detected (rare case)
- **Cost**: 1 extra API call per English response (worst case)
- **Speed**: Negligible - language check is lightweight regex
