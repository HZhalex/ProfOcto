# Logging Guide for ProfOcto

## How Logging Works

Every debate session creates detailed logs to help with debugging and analysis.

### Log Files Created

When you run a debate, **5 log files** are automatically created in the `logs/` folder:

1. **session_TOPIC_TIMESTAMP.log** - Main session log
   - Debate initialization
   - Turn-by-turn progress
   - API calls
   - Final metrics

2. **theorems_TOPIC_TIMESTAMP.log** - Theorem extraction logs
   - Which theorems extracted from each professor
   - Number of theorems, formulas, assumptions found
   - Math density scores
   - Extraction errors

3. **rigor_TOPIC_TIMESTAMP.log** - Mathematical rigor scoring logs
   - Rigor scores for each turn
   - Breakdowns: theorem citations, proof density, citation quality, logical consistency
   - Verdicts assigned to each professor

4. **gaps_TOPIC_TIMESTAMP.log** - Research gap detection logs
   - Which gaps were identified
   - Gap types and difficulty levels
   - PhD value assessment
   - Gap detection progress

5. **errors_TOPIC_TIMESTAMP.log** - Error log
   - All errors from any component
   - Stack traces for debugging
   - API failures
   - JSON parsing errors

### Viewing Logs

After debate completes, you'll see:

```
📋 LOG FILES CREATED

Session logs: logs/session_Tensor_Parallelism_20260317_120000.log
Theorem logs: logs/theorems_Tensor_Parallelism_20260317_120000.log
Rigor logs: logs/rigor_Tensor_Parallelism_20260317_120000.log
Gap logs: logs/gaps_Tensor_Parallelism_20260317_120000.log
Error logs: logs/errors_Tensor_Parallelism_20260317_120000.log

All logs in: logs/
```

### Example Log Content

**session log:**

```
2026-03-17 12:00:00 - profocto.session - [INFO] - === DEBATE START ===
2026-03-17 12:00:00 - profocto.session - [INFO] - Topic: Tensor Parallelism vs Pipeline Parallelism
2026-03-17 12:00:00 - profocto.session - [INFO] - Professors: [Prof A, Prof B]
2026-03-17 12:00:05 - profocto.session - [DEBUG] - API Call: theorem_extractor | Model: gemma-3-1b-it | Prompt: 450 chars
2026-03-17 12:00:10 - profocto.session - [DEBUG] - API Response: theorem_extractor | 1200 chars | Status: OK
```

**rigor log:**

```
2026-03-17 12:00:15 - profocto.rigor - [INFO] - >> Scoring mathematical rigor for Prof A
2026-03-17 12:00:20 - profocto.rigor - [INFO] - ✓ Prof A scoring complete:
2026-03-17 12:00:20 - profocto.rigor - [INFO] -   - Score: 7.5/10
2026-03-17 12:00:20 - profocto.rigor - [INFO] -   - Verdict: RIGOROUS
2026-03-17 12:00:20 - profocto.rigor - [INFO] -   - Theorem citations:      2.20/3
2026-03-17 12:00:20 - profocto.rigor - [INFO] -   - Proof density:          2.00/3
```

**gaps log:**

```
2026-03-17 12:00:30 - profocto.gaps - [INFO] - >> Identifying research gaps from 4 turns
2026-03-17 12:00:35 - profocto.gaps - [INFO] - ✓ Gap 0 | theoretical_contradiction:
2026-03-17 12:00:35 - profocto.gaps - [INFO] -   - Title: Complexity Bound Discrepancy
2026-03-17 12:00:35 - profocto.gaps - [INFO] -   - Difficulty: PhD
2026-03-17 12:00:35 - profocto.gaps - [INFO] -   - PhD Value: High
2026-03-17 12:00:40 - profocto.gaps - [INFO] - ✓ Research gap detection complete: 3 gaps identified
```

## Debugging with Logs

### If something goes wrong:

1. **Check error logs first:**

   ```bash
   tail -50 logs/errors_*.log  # See last 50 errors
   ```

2. **Check which component failed:**
   - theorem*extractor errors → check theorems*\*.log
   - rigor*scorer errors → check rigor*\*.log
   - gap*identifier errors → check gaps*\*.log

3. **Look at API calls/responses:**
   - Check session\_\*.log for API call details
   - Look for "Status: ERROR" lines

4. **Full trace:**
   - Errors are logged with full Python stack traces in error log
   - Copy the error message to understand what failed

### Example: Debugging Theorem Extraction

If theorem extraction fails for a professor:

**In theorems log:**

```
[ERROR] ✗ Failed to extract theorems from Prof A
[ERROR]   Error: JSON decode error
[ERROR]   Traceback: ...
```

**In error log:**

```
[ERROR] Theorem extraction | Prof A | JSON decode error
Traceback:
  File "agents/theorem_extractor.py", line 45, in extract_theorems
    result = json.loads(result_json)
json.JSONDecodeError: ...
```

### Clean up old logs

```bash
# Remove logs older than 7 days
Remove-Item logs/* -Filter "*.log" -Force  # PowerShell

# Or manually delete specific ones
rm logs/session_*.log logs/error_*.log
```

## Configuration

All logging is automatic and enabled by default. To control logging:

In `config.py`:

```python
# Log levels can be controlled via Python's logging module
# (Currently set to DEBUG level for detailed logging)
```

## Best Practices

1. **Always save logs for research sessions** - They contain valuable data about which theorems were extracted, rigor scores, and identified gaps

2. **Share logs when reporting issues** - If something doesn't work, include the logs folder

3. **Review logs after debates** - Look at `rigor_*.log` to see why a professor got a particular rigor score

4. **Check gaps log** - Verify that research gaps were correctly identified

---

**Reminder:** Logs are NOT committed to git (they're in .gitignore) but they're very useful for local debugging!
