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

---

## 2. Directory Structure & Key Files

```
AINativeSlide/
├── AGENTS.md                       # This file (AI coding agent instructions)
├── SKILL.md                        # Antigravity / Agent Skill definition file
├── README.md / README_EN.md        # User-facing documentation (JA / EN)
├── index.html                      # GitHub Pages root & 16:9 interactive showcase
├── resources/
│   ├── template_base.html          # Clean base template skeleton for new decks
│   ├── speech_script_example.md    # Speaker script document example
│   └── design_templates/           # Corporate / custom HTML templates
├── scripts/
│   ├── verify_slide.py             # Automated quality & layout regression checker
│   └── export_pdf.js               # Headless Puppeteer PDF export script
└── .agents/skills/ainativeslide/   # Workspace agent skill mirror (MUST be synced)
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
If `SKILL.md`, `resources/`, or any core documentation changes, keep `.agents/skills/ainativeslide/` in exact sync:
```bash
rsync -av --delete --exclude '.git' --exclude 'node_modules' --exclude '.DS_Store' /Users/takumi/dev/AINativeSlide/ /Users/takumi/dev/.agents/skills/ainativeslide/
```

### 3. Verification of PDF Export (Optional/Headless)
If Node.js and Puppeteer are available:
```bash
node scripts/export_pdf.js index.html output.pdf
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
- Never exceed 500–600 Japanese characters per slide (or ~900 characters for A4 portrait) to prevent vertical text overflow.

### Rule 3: Zero-Margin Print CSS Preservation
The following print block must never be broken:
```css
@media print {
  @page {
    size: 16in 9in; /* or 4in 3in / A4 landscape / A4 portrait */
    margin: 0;
  }
  body {
    background: transparent !important;
    padding: 0 !important;
  }
  .slide {
    page-break-after: always;
    page-break-inside: avoid;
    box-shadow: none !important;
    border-radius: 0 !important;
    margin: 0 auto !important;
  }
  .no-print {
    display: none !important;
  }
}
```

### Rule 4: Zero External JS Runtime Dependencies
- Do NOT introduce npm packages, Vue, React, Chart.js, Mermaid CDN, or external styling frameworks.
- Charts must be built using **inline SVG** (see SVG templates in `resources/template_base.html`).
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
  - `AINativeSlide-Template-Builder` (Repo: `../AINativeSlide-Template-Builder/`, Skill: `.agents/skills/ainativeslide-template-builder/`) converts corporate presentation templates (PPTX, PDF, Keynote, screenshots) into AINativeSlide-compliant design templates (`resources/design_templates/corporate_default.html`).
- **Zero Drift Specification**:
  - Whenever you modify the base skeleton (`resources/template_base.html`), toolbar UI buttons, script functions, CSS print rules, or localStorage logic in this repo, you **MUST ensure full parity** with `AINativeSlide-Template-Builder`.
  - Corporate design templates generated by the Template Builder must always pass `scripts/verify_slide.py` with zero errors.
  - Never allow feature drift (e.g., leaving deprecated buttons or outdated event handlers) between the two repositories.

---

## 5. Definition of Done for PRs / Changes

Before marking any task as complete:
1. `python3 scripts/verify_slide.py` passes with zero errors on all affected HTML files.
2. If `resources/template_base.html` or core UI logic changed, verify and mirror compatibility with `AINativeSlide-Template-Builder`.
3. `rsync` sync to `.agents/skills/ainativeslide/` (and `.agents/skills/ainativeslide-template-builder/` if relevant) is completed.
4. Git commit messages follow standard Conventional Commits (e.g., `feat: ...`, `fix: ...`, `refactor: ...`, `docs: ...`).
