# NativeSlide (Next-Gen Web-Native HTML Presentation System)

<p align="left">
  <strong>🌐 Language:</strong>
  <a href="README_EN.md"><strong>English</strong></a> | 
  <a href="README.md">日本語 (Japanese)</a>
</p>

> **Break Free from PowerPoint** —— An executive presentation system that leverages a single self-contained HTML file (Single-File HTML) and Tailwind CSS to enable browser-based direct editing, fullscreen presentation mode, speaker notes, and one-click zero-margin PDF export.

---

## 📖 Table of Contents
1. [Philosophy & Key Advantages](#philosophy--key-advantages)
2. [Implemented Features](#implemented-features)
   - [1. Dedicated Presenter View & Stage Timer](#1-dedicated-presenter-view--stage-timer)
   - [2. LocalStorage Auto-Save & Recovery](#2-localstorage-auto-save--recovery)
   - [3. Autonomous AI Quality Testing (Zero-Dependency Python CLI)](#3-autonomous-ai-quality-testing-zero-dependency-python-cli)
   - [4. Fullscreen Presentation Mode (Slideshow)](#4-fullscreen-presentation-mode-slideshow)
   - [5. Speaker Notes](#5-speaker-notes)
   - [6. Table of Contents & Slide Index (TOC Drawer)](#6-table-of-contents--slide-index-toc-drawer)
   - [7. In-Browser Direct Text Editing & Floating Formatting Bar](#7-in-browser-direct-text-editing--floating-formatting-bar)
   - [8. Global Typography Scaling (Font Sizing)](#8-global-typography-scaling-font-sizing)
   - [9. Corporate Design Templates (CI/VI Compliance & PPTX Migration)](#9-corporate-design-templates-civi-compliance--pptx-migration)
   - [10. Inline SVG Business Charts & Comparison Matrix Tables](#10-inline-svg-business-charts--comparison-matrix-tables)
   - [11. Per-Slide Feedback Comments & AI Iteration Loop](#11-per-slide-feedback-comments--ai-iteration-loop)
   - [12. AI Concept Imagery & Drag-and-Drop Image Replacement](#12-ai-concept-imagery--drag-and-drop-image-replacement)
   - [13. Strict Aspect Ratio Control (16:9 / 4:3) & Zero-Margin PDF Print](#13-strict-aspect-ratio-control-169--43--zero-margin-pdf-print)
   - [14. Buttonless Automatic Language Adaptation](#14-buttonless-automatic-language-adaptation)
3. [Keyboard Shortcuts](#keyboard-shortcuts)
4. [Directory & File Structure](#directory--file-structure)
5. [Installation Methods](#installation-methods)
6. [User Guide: Working with AI (ChatGPT, Claude, Gemini, Antigravity, Cursor)](#user-guide-working-with-ai-chatgpt-claude-gemini-antigravity-cursor)
7. [License](#license)


---

## Philosophy & Key Advantages

Traditional presentation tools often suffer from font discrepancies across devices, expensive license requirements, collaboration conflicts, and inconsistent styling. NativeSlide solves these issues by building entirely on open Web standards (HTML5 + Tailwind CSS CDN + Google Fonts + Vanilla JS).

- **100% Self-Contained Single-File HTML**: No Node.js, npm, bundlers, or local servers required. Simply double-click to open in any modern browser, edit directly, and present instantly.
- **Strict Brand Governance (CI/VI Compliance)**: Eliminates arbitrary user color tweaks. Slides are generated strictly from corporate design templates (`resources/design_templates/`) matching your organization's official brand guidelines.
- **Seamless AI Iteration**: Features dedicated per-slide feedback inputs and a one-click copy button that formats your notes into structured prompt instructions ready for any LLM (ChatGPT, Claude, Gemini, Antigravity, Cursor, etc.).

---

## Implemented Features

### 1. Dedicated Presenter View & Stage Timer
Click the **"Presenter"** button in the header or hit **`P`** or **`S`** on your keyboard to open a dual-monitor speaker window.
- **Hidden Notes**: Project only the slide deck on the presentation screen/Zoom share while viewing presenter tools on your laptop.
- **Presenter Features**:
  - **Current Slide**: Real-time scaled preview of what the audience sees.
  - **Next Slide Preview**: Know what is coming next at a glance.
  - **Large-Text Speaker Notes**: High-contrast, easy-to-read talking points with `A-` / `A+` font scaling (edits made here immediately sync back to the main deck).
  - **Stage Timer**: Elapsed time (`MM:SS`), configurable target countdown (5/10/15/20/30 min), pause, and reset. Turns amber at 2 minutes remaining and flashes red when overtime.
- **Zero-Server Local Sync**: Communicates using browser-native `BroadcastChannel` API without any internet or server dependencies.

### 2. LocalStorage Auto-Save & Recovery
All text edits made directly on the slide, as well as speaker notes, feedback comments, and font scales, are automatically persisted to your browser's `localStorage` in real time.
- **Zero Data Loss**: Accidentally reloading (F5) or closing the tab preserves your work immediately.
- **One-Click Reset**: Click the "Reset" button in the header at any time to discard changes and revert to the original HTML.

### 3. Autonomous AI Quality Testing (Zero-Dependency Python CLI)
Before delivering code to the user, the AI executes background validation to autonomously test and repair any defects.
- **Zero Dependencies**: Pure Python 3 script ([`scripts/verify_slide.py`](scripts/verify_slide.py)) utilizing only the standard library.
- **Rigorous Checks**:
  - 1:1 matching between slide count and metadata boxes (`slide-meta-box`).
  - Sequence integrity, missing slide indices, and duplicate checks.
  - **Character Overflow Heuristic**: Detects potential vertical overflow (>700 characters per 16:9 720px slide).
  - UI ID integrity (Header, tabs, TOC drawer, presenter view, zero-margin print CSS).
- **Zero Human Debugging Burden**: The AI reads the CLI error output, autonomously rebalances text density, and delivers only validated code passing with Exit Code 0.

### 4. Fullscreen Presentation Mode (Slideshow)
Press the **"▶ Present"** button in the header or hit **`F`** on your keyboard to launch presentation mode.
- **Smart Aspect-Ratio Auto-Fit**: Uses CSS `transform: scale()` to dynamically center and maximize slides to fill any display resolution while strictly preserving the aspect ratio (16:9 or 4:3).
- **Smooth Navigation**:
  - `→` / `↓` / `Space` / `PageDown` / Click right side: Next slide
  - `←` / `↑` / `PageUp` / Click left side: Previous slide
- **Laser Pointer (`L` key)**: Replaces the cursor with a glowing red laser dot for highlighting key points.
- **Instant Exit (`Esc` key)**: Quickly return to the standard editing mode at any time.

### 5. Speaker Notes
Each slide includes a tabbed metadata box positioned directly below the canvas.
- **During Preparation & Editing**: Click the **"🎤 Speaker Notes"** tab to draft talking points and presenter scripts (`contenteditable="true"`).
- **During Live Presentation**: Press **`N`** to toggle a translucent dark overlay displaying your speaker notes for the current slide.
- **Print-Safe**: Speaker notes and feedback panels are automatically hidden when printing or exporting to PDF via `@media print`.

### 6. Table of Contents & Slide Index (TOC Drawer)
Click the **"☰ Menu"** button on the top-left to slide out a smooth drawer navigation.
- **Automatic Heading Detection**: Dynamically scans `h1` and `h2` headings across all slides to generate titles and slide numbers.
- **One-Click Jump**: Click any title to jump directly to that slide (scrolls in edit mode, switches instantly in presentation mode).

### 7. In-Browser Direct Text Editing & Floating Formatting Bar
- **Direct Editing**: Click any text element on the slide to edit it immediately.
- **Floating Mini Toolbar**: Selecting text automatically reveals a floating format bar above the selection (Bold, font scaling, highlighter, clear formatting).

### 8. Global Typography Scaling (Font Sizing)
- **Global Typography Scaling**: Adjust slide font sizes from 85% to 125% using the header `[A-]` `100%` `[A+]` controller to optimize readability for any room size or projector resolution.

### 9. Corporate Design Templates (CI/VI Compliance & PPTX Migration)
To enforce enterprise branding and prevent arbitrary styling divergences, casual color palette pickers have been eliminated.
- **Separation of Structure & Brand**: Grounded in [`resources/design_templates/corporate_default.html`](./resources/design_templates/corporate_default.html) with standardized CI colors, company logo, confidentiality pill, and footer positioning.
- **Migrating Existing PPTX Decks**: Organizations with official PowerPoint templates can convert and register their design once using the setup skill [nativeslide-template-builder](https://github.com/XitakSE/NativeSlide-Template-Builder). Once registered, the AI produces decks with the official company look and feel automatically.

### 10. Inline SVG Business Charts & Comparison Matrix Tables
- **Zero-Dependency Pure Inline SVG**: Render high-contrast bar and line combo charts directly within the single-file HTML without external libraries like Chart.js.
- **Sophisticated Matrix Tables**: Option A vs Option B vs Option C (Recommended) evaluation grids with clear badges, border highlights, and symbols (◎, ◯, ▲, ✕).

### 11. Per-Slide Feedback Comments & AI Iteration Loop
- Enter specific change requests into the **"💬 Feedback"** tab under any slide (e.g., "Shorten this bullet point", "Wrap text cleanly", "Update quarterly metrics").
- **"📋 Copy Instructions"**: Automatically formats all comments across slides into an organized prompt and copies it to your clipboard. Paste it directly into your AI chat to request the updated HTML.
- **"📥 Save HTML"**: Download the current HTML with all your edits and comments preserved.

### 12. AI Concept Imagery & Drag-and-Drop Image Replacement
- Pre-configured prompt templates for AI image generators (DALL-E 3, Midjourney, Imagen) tailored for abstract business concepts (system architectures, pipelines, data unifications) without garbled text.
- Drag-and-drop any image from your desktop directly onto a slide's `.image-dropzone` to instantly replace it.

### 13. Strict Aspect Ratio Control (16:9 / 4:3) & Zero-Margin PDF Print
- Designed with `@page { size: 16in 9in; margin: 0; }` and `.slide { page-break-inside: avoid; }` to produce pixel-perfect, margin-free PDF exports using your browser's Print dialog ("Save as PDF").

### 14. Buttonless Automatic Language Adaptation
To prevent UI clutter and keep the toolbar minimal and focused, there are no manual language switch buttons.
- **Japanese Prompts**: The AI generates slides with `<html lang="ja">`, creating Japanese headings, content, and annotations.
- **Non-Japanese Prompts (English, etc.)**: The AI generates slides with `<html lang="en">`. The embedded JavaScript silently and automatically localizes all UI controls (Menu, Presenter, Copy Feedback, Save HTML, Present, Save PDF), TOC drawer (Table of Contents), meta box tabs (Feedback, Speaker Notes), input placeholders, and AI revision copy formats (`【Slide X Feedback】`) into clean English.

---

## Keyboard Shortcuts

| Key | Mode | Action |
| :--- | :--- | :--- |
| **`P`** / **`S`** | Edit / Present | Launch / focus dedicated **Presenter View** in a separate window |
| **`F`** / **`F5`** | Edit / Present | Start / Stop fullscreen presentation mode |
| **`Esc`** | Present / Drawer | Exit presentation mode or close TOC drawer |
| **`→`** / **`↓`** / **`Space`** / **`PageDown`** | Present / Speaker | Next slide (syncs main deck and speaker view) |
| **`←`** / **`↑`** / **`PageUp`** | Present / Speaker | Previous slide (syncs main deck and speaker view) |
| **`N`** | Present | Toggle in-slide speaker notes overlay |
| **`L`** | Present | Toggle red laser pointer mode |

*Note: Shortcuts are automatically disabled when typing in input boxes or active `contenteditable` elements to prevent interference.*

---

## Directory & File Structure

```
NativeSlide/
├── SKILL.md                 # AI Agent Skill specification (Smart Grill, Auto-Verification loop)
├── README.md                # Japanese documentation (Comprehensive user & enterprise guide)
├── README_EN.md             # English documentation
├── scripts/
│   └── verify_slide.py      # [Zero-Dependency] Pure Python 3 auto-verification & quality test tool
├── resources/
│   ├── template_base.html   # Fully functional base HTML template (Feature Engine)
│   └── design_templates/   # Corporate brand design templates (CI/VI compliance)
│       └── corporate_default.html # Default corporate brand template (CI colors, logo, badges)
├── examples/                # Complete interactive slide examples
│   ├── slide_16_9_example.html     (16:9 Japanese sample, 8 slides, charts & tables)
│   ├── slide_16_9_en_example.html  (16:9 English sample)
│   └── slide_4_3_example.html      (4:3 Japanese sample)
└── references/              # Detailed specifications & guidelines
    ├── grill-workflow.md    # Cognitive alignment interview specification
    ├── ratio-and-print-specs.md # 16:9 / 4:3 aspect ratio & print CSS specs
    ├── ai-concept-imagery.md # Concept image generation prompt guidelines
    ├── design-system.md     # Typography & robust card box model specs
    └── slide-patterns.md    # Reusable slide layout patterns (Tables & SVG Charts)
```

---

## Installation Methods

In AI agent environments such as Antigravity, Claude Code, or Cursor, NativeSlide is automatically recognized as an agent skill when placed inside the `.agents/skills/` directory.

### Method 1: Git Clone (Recommended)

```bash
git clone https://github.com/XitakSE/NativeSlide.git .agents/skills/nativeslide
```

### Method 2: Direct ZIP Download (Enterprise Firewalls & No Git CLI)

If your enterprise network restricts external `git clone` or you do not have Git installed:

1. Click **"<> Code" ➔ "Download ZIP"** on the [NativeSlide GitHub page](https://github.com/XitakSE/NativeSlide).
2. Extract the downloaded ZIP file.
3. Rename the extracted folder (`NativeSlide-main`) to `nativeslide` and place it directly into your workspace's `.agents/skills/nativeslide` directory.
   *(Make sure `SKILL.md` is located directly inside the folder).*

---

## User Guide: Working with AI (ChatGPT, Claude, Gemini, Antigravity, Cursor)


When using NativeSlide in enterprise AI environments (ChatGPT Enterprise, Claude for Work, Google Gemini, Antigravity, Cursor, etc.) where Skill integration is available, **users do NOT need to upload or manage template files manually**.

The AI agent will automatically load the skill, inspect `resources/template_base.html` and `resources/design_templates/`, generate the single-file presentation, run `scripts/verify_slide.py` in the background, and fix any layout or numbering issues before delivering the final HTML code.

```mermaid
flowchart TD
    A[User: 'Create an executive presentation on XYZ'] --> B[AI loads NativeSlide skill]
    B --> C[Inspects template_base.html & corporate_default.html]
    C --> D[Generates Single-File Presentation HTML]
    D --> E[Runs background validation: scripts/verify_slide.py]
    E --> F{Test Suite Passed?<br/>Exit Code 0?}
    F -- Failure / Overflow --> G[AI autonomously adjusts character count & indices]
    G --> E
    F -- Success (Exit 0) --> H[🚀 Delivers polished HTML directly to chat<br/>(Zero debugging burden on user)]
```

---

### 1. Slide Generation Prompt Example

Provide your topic and high-level requirements in your AI chat:

```markdown
Please create an executive presentation using NativeSlide (Single-File HTML format).

[Topic]
Enterprise Modern Data Stack & Next-Gen Data Platform Strategy

[Target Audience]
C-level Executives & Board of Directors (Focus on ROI, governance, and phased execution)

[Requirements]
1. Aspect Ratio: 16:9 Widescreen (Default)
2. Slide Count: 6-8 slides
3. Key Components:
   - Title Slide (Corporate badge & confidential pill)
   - AS-IS vs TO-BE Architecture comparison card
   - Evaluation matrix comparing 3 approaches (highlight recommended option)
   - 4-Year ROI projection chart (Inline SVG business chart)
   - 4-Phase rollout roadmap
   - Executive KPIs & Business Outcomes
4. Include detailed speaker talking notes in the notes section of each slide.
```

---

### 2. Browser Review & AI Iteration Loop

Save the generated code as `slide.html` and open it in Google Chrome, Microsoft Edge, or Safari:

1. **Direct Editing**: Click any text on the slide to edit directly. Changes are automatically saved to `localStorage`.
2. **Slide-Specific Feedback**: Click the **"💬 Feedback"** tab under any slide to enter revision notes (e.g., "Change target metric to 35%", "Shorten summary by one sentence").
3. **Batch Instructions**: Click **"📋 Copy Instructions"** in the toolbar, then paste it into your AI chat:

```markdown
Please revise the presentation HTML according to the following slide comments.
Preserve all text, colors, and styling from unmodified slides exactly as edited in the browser:

(Paste copied clipboard content here)
```

---

### 3. Presenting & Exporting to PDF

- **Presenting Live**:
  - Hit **`P`** to launch **Presenter View** on your laptop screen (notes, next slide preview, live timer).
  - Hit **`F`** to launch full-screen slideshow on the projector or Zoom screen share.
- **Exporting to PDF**:
  - Click **"Save PDF"** in the toolbar (or press `Ctrl+P` / `Cmd+P`).
  - Set destination to **"Save as PDF"**, Margins to **"None"**, and enable **"Background graphics"**.

---

### 4. Enterprise AI System Instructions (GPTs / Claude Projects / Gems)

To configure an enterprise-wide presentation assistant in OpenAI Custom GPTs, Anthropic Claude Projects, or Google Gemini Gems, add the following prompt to the assistant's System Instructions:

```text
You are an executive presentation designer. When asked to create presentations or slide decks, create web-native HTML presentations following the NativeSlide specification.

[Guidelines]
1. Output a valid, complete Single-File HTML complying with the NativeSlide specification (Tailwind CSS CDN, Google Fonts, Presenter View, Stage Timer, LocalStorage auto-save, Segmented Edit/Present toolbar).
2. Use `resources/template_base.html` for functional engine architecture and `resources/design_templates/corporate_default.html` for corporate brand styling.
3. If essential requirements are ambiguous, clarify Audience, Ratio (16:9 recommended), and Slide Count concisely using Smart Grill.
4. Set each slide to contenteditable="true" and include meta boxes for "Feedback" and "Speaker Notes".
5. Use modern Tailwind color palettes (Slate + Indigo/Violet) and robust card box models (flex-shrink-0, min-h-0).
6. [Auto-Verification]:
   Before returning HTML to the user, run `python3 scripts/verify_slide.py <file.html>` in your background environment. Fix any character overflows (>700 chars) or slide index mismatches autonomously, and only deliver code that achieves Exit Code 0 (all tests passed).
```

---

## License

MIT License © 2026 NativeSlide Contributors. Free for commercial and personal use.
