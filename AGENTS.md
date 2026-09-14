# AGENTS.md

This document provides essential context, architectural rules, and verification workflows for AI coding agents (such as Jules, Gemini Code Assist, Claude Code, Cursor, and others) working on the **AINativeSlide** repository.

---

## 1. Project Overview & Philosophy

**AINativeSlide** is an AI output stabilization framework for creating high-impact, pixel-perfect presentation slide decks as a **Single-File HTML** with zero-margin PDF printing (16:9 or 4:3).

### Core Principles
1. **HTML & Tailwind CSS First**: Leveraging standard HTML5 and Tailwind CSS—the format LLMs generate most reliably—rather than fragile AST-based formats (like pptx or Marp).
2. **Single-File Zero-Dependency**: Everything (Tailwind CDN, inline SVG charts, Lucide icons, scripts) is self-contained in one file. No heavy runtime chart libraries (like Chart.js or D3) and no presentation frameworks (like Reveal.js).
3. **Interactive Human-in-the-Loop Refinement**:
   - `contenteditable` browser-side text editing with real-time `localStorage` autosave.
   - Per-slide feedback comments (`.slide-comment-input`) with a one-click clipboard copy (`📋 指示をコピー` / `Copy Instructions`) to feed changes back to AI.
   - Decoupled presentation speech script (`speech_script.md`) for speaker notes.
4. **Zero-Margin PDF Printing**: Built-in CSS `@page` print rules to guarantee exact slide-to-page margins on standard browser print (`Cmd+P` / `Ctrl+P`).

### Enterprise Deployment Context: Non-IDE, Skill-Enabled Environments
In typical corporate enterprise deployments (e.g., ChatGPT Enterprise, Claude for Work / Projects, internal secure AI web portals):
- **No Developer IDE or CLI Access**: Business users cannot run terminal commands, local Python scripts, or developer IDEs (Cursor, VS Code).
- **No External LLM API Calls**: Strict enterprise network and data egress security policies prohibit calling external APIs (e.g., calling Gemini API via Python `urllib` or curl).
- **Skill Specifications Are Fully Functional**: AI agents operating inside enterprise web chats can read and follow **Agent Skills (`SKILL.md` and `references/`)** as their core system instructions.
- **Architectural Implication**:
  - Quality enforcement cannot solely rely on Python scripts or secondary API calls.
  - **The primary generation AI agent itself must perform autonomous semantic reflection (Approach B)** using the guardrails and self-evaluation checklists in `SKILL.md` and `references/slide-patterns.md`.
  - Python tools like `scripts/verify_slide.py` serve as zero-dependency local safety nets for developer environments and CI/CD pipelines, using forgiving heuristics rather than brittle, rigid word-match lists.

---

## 2. Directory Structure & Key Files

```
AINativeSlide/
├── .github/workflows/
│   └── gemini-pr-review.yml        # Automated Gemini Code Assist PR review workflow
├── AGENTS.md                       # This file (AI coding agent instructions)
├── CLAUDE.md                       # Claude Code CLI entrypoint directives
├── SKILL.md                        # Antigravity / Agent Skill definition file
├── README.md / README_EN.md        # User-facing documentation (JA / EN)
├── index.html                      # GitHub Pages root & 16:9 interactive showcase
├── agents/                         # Multi-Agent manifest definitions
│   └── openai.yaml                 # OpenAI Agent / ChatGPT specification
├── assets/                         # Standard Agent Skills assets directory
│   ├── template_base.html          # Clean base template skeleton for new decks
│   ├── speech_script_example.md    # Speaker script document example
│   └── design_templates/           # Corporate / custom HTML templates
├── references/                     # Detailed technical specifications
│   ├── grill-workflow.md           # Cognitive-drift prevention grill protocol
│   ├── ratio-and-print-specs.md    # Aspect ratios & zero-margin print CSS specs
│   ├── ai-concept-imagery.md       # AI concept imagery prompt engineering
│   ├── design-system.md            # Typography & robust box-model guidelines
│   └── slide-patterns.md           # Information structuring, layout patterns, and SVG charts
└── scripts/
    ├── verify_slide.py             # Automated quality & layout regression checker
    └── gemini_pr_review.py         # Automated Gemini PR review script
```

### Related Companion Projects
- **`AINativeSlide-Template-Builder`** (`/Users/takumi/dev/AINativeSlide-Template-Builder/`):
  - Companion skill for converting corporate slide templates (PPTX, PDF, Keynote, screenshots) into AINativeSlide design templates.
  - Workspace Skill Mirror: `.agents/skills/ainativeslide-template-builder/`

---

## 3. Essential Commands & Verification Workflows

Whenever you modify any slide HTML, templates, or scripts, you **MUST** run the following verification steps:

### 1. Slide Quality Verification (Automated Regression Test)
Always run `scripts/verify_slide.py` against modified HTML files:
```bash
python3 scripts/verify_slide.py index.html
```
- **Exit Code 0**: Required before presenting any HTML file to the user or submitting a PR.
- If the exit code is `1`, read the `[ERROR]` messages, fix the issue in the HTML, and re-run until all tests pass.

### 2. Synchronization to Workspace Skills
If `SKILL.md`, `assets/`, or any core documentation changes, keep `.agents/skills/ainativeslide/` in exact sync:
```bash
rsync -av --delete --exclude '.git' --exclude 'node_modules' --exclude '.DS_Store' /Users/takumi/dev/AINativeSlide/ /Users/takumi/dev/.agents/skills/ainativeslide/
```

---

## 4. Golden Architectural Rules for AI Agents

When editing or generating slide decks in this repository, strictly adhere to these rules:

### Rule 1: Maintain the 1:1 Slide & Meta Box Relationship
- Every `<section class="slide ...">` MUST be directly followed by exactly one `<div class="slide-meta-box no-print ...">`.
- The total slide count (`#deckSlideCountText`), the footer slide numbering (`01 / 08`), and the meta-box count must match 100%.

### Rule 2: Strict Aspect Ratio and Overflow Prevention
- **16:9 ワイド**: Dimensions MUST be `w-[1280px] h-[720px] max-w-[1280px] max-h-[720px]` with `overflow-hidden`.
- **4:3 スタンダード**: Dimensions MUST be `w-[1024px] h-[768px] max-w-[1024px] max-h-[768px]` with `overflow-hidden`.
- **A4 横 (Landscape)**: Dimensions MUST be `w-[1188px] h-[840px] max-w-[1188px] max-h-[840px]` with `overflow-hidden`.
- **A4 縦 (Portrait)**: Dimensions MUST be `w-[840px] h-[1188px] max-w-[840px] max-h-[1188px]` with `overflow-hidden`.
- Recommended text length is 500–600 Japanese characters per slide (or ~850 characters for A4 portrait). Never exceed the hard limit of 700 characters (or 1,100 characters for A4 portrait) enforced by `scripts/verify_slide.py` to prevent vertical text overflow.

### Rule 3: Zero-Margin Print CSS Preservation
The following print block (top-level `@page` and `@media print`) must never be broken:
```css
@page {
  size: 16in 9in; /* or 4in 3in / A4 landscape / A4 portrait */
  margin: 0;
}
@media print {
  body {
    background: transparent !important;
    margin: 0 !important;
    padding: 0 !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  .no-print {
    display: none !important;
  }
  .slide-viewport {
    padding: 0 !important;
    gap: 0 !important;
    display: block !important;
  }
  .slide {
    width: 16in !important;
    height: 9in !important;
    max-width: none !important;
    max-height: none !important;
    page-break-after: always !important;
    break-after: page !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    margin: 0 auto !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    border: none !important;
  }
}
```

### Rule 4: Zero External JS Runtime Dependencies
- Do NOT introduce npm packages, Vue, React, Chart.js, Mermaid CDN, or external styling frameworks.
- Charts must be built using **inline SVG** (see SVG templates in `assets/template_base.html`).
- Icons must be inline SVG or minimal Lucide script.

### Rule 5: No In-Slide HTML Download Button
- Do NOT re-introduce a browser Blob download button (`downloadHtmlWithComments` or `📥 HTML保存`) in the slide header toolbar.
- AI chat environments (ChatGPT Canvas, Claude Artifacts, Antigravity IDE, Cursor) provide their own file download capabilities.
- The toolbar should remain focused on:
  1. `[📝 編集: ON  E]` (Toggle edit mode)
  2. `[📋 指示をコピー]` (Copy all feedback comments to clipboard)
  3. `[▶ 全画面発表  F]` (Fullscreen slideshow)
  4. `[🖨 PDF保存]` (Browser print dialog)

### Rule 6: Full Parity & Consistency with AINativeSlide-Template-Builder
- **Companion Sub-Skill / Sister Project**:
  - `AINativeSlide-Template-Builder` (Repo: `../AINativeSlide-Template-Builder/`, Skill: `.agents/skills/ainativeslide-template-builder/`) converts corporate presentation templates (PPTX, PDF, Keynote, screenshots) into AINativeSlide-compliant design templates (`assets/design_templates/corporate_default.html`).
- **Zero Drift Specification**:
  - Whenever you modify the base skeleton (`assets/template_base.html`), toolbar UI buttons, script functions, CSS print rules, or localStorage logic in this repo, you **MUST ensure full parity** with `AINativeSlide-Template-Builder`.
  - Corporate design templates generated by the Template Builder must always pass `scripts/verify_slide.py` with zero errors.
  - Never allow feature drift (e.g., leaving deprecated buttons or outdated event handlers) between the two repositories.

### Rule 7: Anti-AI-Smell Guardrails & Structured Wireframes
When generating slide content, strictly avoid generic "AI-smelling" outputs:
- **No Equal 3-Card Grids without Visual Anchors**: Never create 3 identical cards. Always highlight recommended options (`CORE`, `推奨`, `border-brand-500`, background pills).
- **No Abstract Buzzwords**: Ban empty buzzwords like "シナジーの最大化", "シームレスな連携", "DX推進の加速", "柔軟な対応". Use concrete verbs and metrics.
- **Autonomous Semantic Reflection (Approach B)**:
  Do not rely on brittle static word lists or secondary API calls to detect vague phrases. Before finalizing HTML output, the agent must internally reflect on the "vibe" and resolution of the text:
  * "If a front-line employee reads this, can they picture who needs to take what physical action tomorrow?"
  * Proactively rewrite high-level corporate slogans (e.g., "最適化を図る", "伴走型支援", "エコシステムの共創") into concrete operational behaviors (e.g., "手動転記フローの廃止", "夜間バッチ同期", "承認者2名体制への移行") and quantitative metrics.
  * Perfection is not demanded, but hollow corporate fluff must be proactively mitigated through self-reflection.
- **Action Titles (Lead Messages) Required**: Slide titles must be complete sentences (40–60 characters) stating fact + insight/conclusion with active verbs, not passive noun labels (like "〇〇について").
- **Structured Wireframe Catalog**: Prefer the 6 enterprise wireframe patterns documented in [`references/slide-patterns.md`](references/slide-patterns.md) (`problem_solution`, `tradeoff_matrix`, `scope_boundary`, `architecture_mapping`, `step_process`, `pitfalls_faq`).

### Rule 8: Semantic Line Breaking & Header Spacing Protection
- **No Awkward Mid-Word Wraps**: Never let Japanese text break awkwardly mid-word or leave trailing particles (1–2 characters) on a new line due to arbitrary container boundary collisions. Always insert explicit `<br>` breaks at natural grammatical phrase boundaries (particles `〜し、`, `〜により、`, `〜から、` or punctuation), or adjust font size/container width.
- **Top-Right Badge Protection**: Top-right slide meta/category badges must NEVER wrap into multiple lines when titles span 2 lines. Always use `shrink-0 whitespace-nowrap` on badge containers and structure headers with `items-start gap-6` (title taking `flex-1 min-w-0 pr-4`).
- **Header-Content Vertical Rhythm**: Never let multi-line Action Titles collapse vertical margins with the main slide content below. Always enforce explicit separation (e.g. `pb-3 border-b border-slate-800 mb-5` or `mb-6`) to guarantee comfortable breathing room and visual hierarchy.

### Rule 9: Pure Single-File Complete Architecture (Mandatory Base64 Inline Images)
- **Zero External Image Dependencies**: Never reference external local paths (`./images/...`, `./demo_assets/...`) or remote CDN URLs in `<img src="...">`.
- **Mandatory Base64 Data URI**: All AI-generated images or user-provided image assets must be converted to Base64 Data URIs (`data:image/jpeg;base64,...` or `data:image/png;base64,...`) and embedded directly into the HTML document.
- **100% Portability**: The resulting HTML slide deck must remain completely self-contained, ensuring that downloading, emailing, or viewing offline will never encounter broken image links (404).

---

## 5. Definition of Done for PRs / Changes

Before marking any task as complete:
1. `python3 scripts/verify_slide.py` passes with zero errors on all affected HTML files.
2. If `assets/template_base.html` or core UI logic changed, verify and mirror compatibility with `AINativeSlide-Template-Builder`.
3. `rsync` sync to `.agents/skills/ainativeslide/` (and `.agents/skills/ainativeslide-template-builder/` if relevant) is completed.
4. Git commit messages follow standard Conventional Commits (e.g., `feat: ...`, `fix: ...`, `refactor: ...`, `docs: ...`).
