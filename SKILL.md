---
name: ainativeslide
description: >-
  Use this skill whenever the user asks to create, design, generate, edit, or format
  presentation slides, pitch decks, corporate proposals (企画書/提案書), executive approval memos (稟議資料),
  Amazon-style 1-Pagers (1枚ペーパー), or zero-margin PDF-printable HTML slides across all supported aspect
  ratios (16:9 widescreen, 4:3 standard, A4 landscape, A4 portrait). Enforces Single-File HTML/Tailwind CSS,
  pure inline SVG charts, automated Python verification, and autonomous self-repair.
---

# AINativeSlide Agent Execution Contract

Execute slide generation strictly following this deterministic sequence. Do NOT deviate.

---

## 1. MANDATORY EXECUTION SEQUENCE

```
[Step 1: Dynamic Grill] ➔ [Step 2: Read Base Skeleton] ➔ [Step 3: Generate HTML] ➔ [Step 4: Verify & Self-Repair] ➔ [Step 5: Deliver]
```

### Step 1: Dynamic Smart Grill (Cognitive Alignment)
Before generating code, check if the prompt specifies these core parameters:
1. **Purpose & Audience**: Executive decision / Team internal / Customer pitch / Printed proposal
2. **Aspect Ratio**:
   - `16:9 Widescreen` (`w-[1280px] h-[720px]` / `@page { size: 16in 9in; }`) [Default for screen presentation]
   - `4:3 Standard` (`w-[1024px] h-[768px]` / `@page { size: 4in 3in; }`)
   - `A4 Landscape` (`w-[1188px] h-[840px]` / `@page { size: A4 landscape; }`) [Recommended for printed proposals/稟議]
   - `A4 Portrait` (`w-[840px] h-[1188px]` / `@page { size: A4 portrait; }`) [Recommended for 1-Pagers/企画書]
3. **Slide Count & Outline**: 3-slide summary / 5-slide standard / Custom
4. **Speaker Script**: Whether to generate a companion Markdown speech script (`speech_script.md`)

> **Decision Rule**:
> - If all parameters are already clear or inferable from context, **SKIP questions entirely**, state your inferred plan in 1 line, and immediately proceed to Step 2.
> - Only ask multiple-choice questions for truly ambiguous points.

### Step 2: Read Base Skeleton
- **MANDATORY**: You MUST inspect [resources/template_base.html](./resources/template_base.html) using `view_file` to obtain the verified header toolbar, modal, and script engine.
- If corporate branding is requested, check [resources/design_templates/corporate_default.html](./resources/design_templates/corporate_default.html).

### Step 3: Generate Single-File HTML
Assemble the complete, self-contained HTML (`<!DOCTYPE html>...</html>`) adhering to these rules:
1. **Header Toolbar**: Keep intact with `[📝 編集: ON]`, `[📋 指示をコピー]`, `[▶ 全画面発表]`, `[🖨 PDF保存]`.
2. **Slide Box Model**: Every slide MUST have class `slide` with fixed dimensions and `overflow-hidden`.
3. **Meta Box**: Every `<section class="slide ...">` MUST be directly followed by `<div class="slide-meta-box no-print ...">` with identical slide numbering.
4. **Content Area**: Wrap slide body in `<div class="ai-content">` using semantic elements (`h2`, `h3`, `p`, `ul`, `li`). Use Tailwind `line-clamp` to eliminate text overflow risk.
5. **Inline SVG**: Render charts and graphics using pure inline `<svg>`. Do NOT load external chart libraries.
6. **Localization**: Set `<html lang="ja">` or `<html lang="en">` based on user prompt language. The template script auto-localizes toolbar labels and placeholders.

### Step 4: Autonomous Verification & Self-Repair Loop
Before presenting the HTML to the user, run the automated quality checker:
```bash
python3 scripts/verify_slide.py <path_to_slide.html>
```
- **If Exit Code is 0**: Verification passed. Proceed to Step 5.
- **If Exit Code is 1**:
  1. Parse the output `[ERROR]` messages (e.g., slide/meta-box count mismatch, missing IDs, character overflow > 700 chars).
  2. Autonomously fix the HTML file without asking the user.
  3. Re-run `python3 scripts/verify_slide.py` until Exit Code 0 is achieved.
  4. Never show raw test failures or debugging churn to the user.

### Step 5: Deliver Output & Handle Iterations
- Output the clean Single-File HTML inside a single markdown code block (`html`).
- If requested in Step 1, output the companion speaker script (`speech_script.md`) referencing [resources/speech_script_example.md](./resources/speech_script_example.md).
- **On User Feedback (Refinement)**:
  - If the user provides comments via the "📋 指示をコピー" clipboard button, preserve unmentioned slides 100% and edit only targeted slides.

---

## 2. NEGATIVE CONSTRAINTS (STRICTLY FORBIDDEN)

1. **NEVER** write arbitrary HTML scaffolding from scratch; ALWAYS base it on [resources/template_base.html](./resources/template_base.html).
2. **NEVER** introduce external JS libraries (Chart.js, D3, Reveal.js, Mermaid CDN, Vue, React).
3. **NEVER** include an in-slide HTML download button or blob download script (`downloadHtmlWithComments` is deleted).
4. **NEVER** violate the 1:1 match between `<section class="slide">` and `.slide-meta-box`.
5. **NEVER** remove or alter the zero-margin print CSS:
   ```css
   @media print {
     @page { margin: 0; }
     body { background: transparent !important; margin: 0 !important; padding: 0 !important; }
     .slide { page-break-after: always !important; page-break-inside: avoid !important; margin: 0 auto !important; }
     .no-print { display: none !important; }
   }
   ```
6. **NEVER** exceed 600–700 Japanese characters per horizontal slide (or 1000 characters for A4 portrait).

---

## 3. DIMENSIONS & PRINT FORMULAS REFERENCE

| Format | Target Use Case | Screen Class | Print CSS `@page` |
| :--- | :--- | :--- | :--- |
| **16:9 Widescreen** | Web presentations, modern monitors | `w-[1280px] h-[720px]` | `@page { size: 16in 9in; margin: 0; }` |
| **4:3 Standard** | Legacy projectors, academic talks | `w-[1024px] h-[768px]` | `@page { size: 4in 3in; margin: 0; }` |
| **A4 Landscape** | Office printed proposals, executive memos (稟議) | `w-[1188px] h-[840px]` | `@page { size: A4 landscape; margin: 0; }` |
| **A4 Portrait** | Amazon-style 1-Pagers, executive summaries | `w-[840px] h-[1188px]` | `@page { size: A4 portrait; margin: 0; }` |
