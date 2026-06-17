# Bypass Curator — Rollback Guide

## Why

Curator was bypassed to always produce a WAV output without rejection/retry.
All disabled code is preserved as comments in the source files.

## How to Restore the Curator

### `src/graph.py`

1. **Line 10**: Uncomment `from src.agents.curator_agent import curator_node`
2. **Lines 27–38**: Uncomment the `decide_next_after_curator` function (between the `# ===` markers)
3. **Lines 41–62**: Uncomment the `error_termination_node` function (between the `# ===` markers)
4. **Line 74**: Change `# graph.add_node("taste_curator", ...)` → `graph.add_node("taste_curator", curator_node)`
5. **Line 75**: Change `# graph.add_node("error_termination", ...)` → `graph.add_node("error_termination", error_termination_node)`
6. **Line 84**: Change `graph.add_edge("audio_analyzer", END)` → `graph.add_edge("audio_analyzer", "taste_curator")`
7. **Lines 86–94**: Uncomment the `graph.add_conditional_edges(...)` block (between the `# ===` markers)
8. **After line 94**: Uncomment `graph.add_edge("error_termination", END)`

### `src/main.py`

9. **Lines 59–76**: Restore the original dry-run text showing 8 nodes + conditional routing
10. **Lines 98–103**: Remove the `if final_state.get("curator_report"):` guard and restore the two unconditional print lines

## Verification

After restoring, run a dry-run to confirm the graph shows taste_curator and error_termination:
```powershell
python src/main.py --dry-run
```
