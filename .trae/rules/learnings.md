# 🐛 LEARNINGS & REFACTORING LOG (ORCHESTRATION HEADER)

> **AGENT INSTRUCTION**: Read this file EXCLUSIVELY when you are executing a bug fix or refactoring an existing system. 
> Do NOT read this file for standard feature development unless specifically directed by PROJECT_RULES.md.
> 
> **Index:**
> - Lines 15-25: How to append new learnings
> - Lines 30+: Logged Bugs & Corrections

---

## How to Append a Learning (Lines 15-25)
When a bug is fixed, append to this file using this exact format:
```markdown
### [YYYY-MM-DD] | [Topic/Service]
- **Bug/Mistake**: What went wrong.
- **Root Cause**: Why it happened.
- **Correction applied**: How it was fixed.
- **Rule alignment**: Was PROJECT_RULES.md updated?
```

---

## Logged Bugs & Corrections (Lines 30+)

### 2026-02-27 | React Hooks
- **Bug/Mistake**: Named a React hook `getWorkoutData()`.
- **Root Cause**: Ignored framework-specific React convention.
- **Correction applied**: Renamed to `useWorkoutData()`.
- **Rule alignment**: Yes, added "React hooks use `use*`" to PROJECT_RULES.md.

### [Template Entry - Delete After First Real Entry]
- **Bug/Mistake**: [Describe what was generated incorrectly]
- **Root Cause**: [Why did this happen? Ambiguous rule? Missing context?]
- **Correction applied**: [Describe the correct implementation]
- **Rule alignment**: [No / Yes — describe change to PROJECT_RULES.md]
