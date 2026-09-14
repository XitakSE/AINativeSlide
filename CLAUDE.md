# CLAUDE.md

This repository defines an AI Agent Skill (**AINativeSlide**) for generating production-grade Single-File HTML presentation slides with zero-margin PDF printing.

## Core Directives for Claude Code

- **Skill Execution (When user requests presentation slides, proposals, or 1-pagers)**:
  - You MUST read and follow [SKILL.md](./SKILL.md) as the primary execution contract.
  - Conduct the mandatory Grill & outline approval before generating HTML.
  - Base all decks on [assets/template_base.html](./assets/template_base.html).
  - Apply Anti-AI-Smell semantic guardrails from [references/slide-patterns.md](./references/slide-patterns.md).
- **Code Quality & Validation**:
  - Run the automated regression verifier whenever modifying slides:
    ```bash
    python3 scripts/verify_slide.py <path_to_slide.html>
    ```
- **Repository Architecture & Rules**:
  - Refer to [AGENTS.md](./AGENTS.md) for full architectural constraints, box-model specs, and multi-agent coordination.
