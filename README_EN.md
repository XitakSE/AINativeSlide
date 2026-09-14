# AINativeSlide (Stable & High-Precision HTML Slide Framework for Generative AI)

<p align="left">
  <strong>🌐 Language:</strong>
  <a href="README_EN.md"><strong>English</strong></a> | 
  <a href="README.md">日本語 (Japanese)</a>
</p>

> **When generating slides with AI, choose HTML over PPTX** —— LLMs generate HTML/Tailwind CSS with the highest precision and layout freedom. AINativeSlide uses HTML as an intermediate scaffolding format to eliminate text overflow and layout glitches, producing pixel-perfect, zero-margin PDF slide decks with autonomous Python verification.

<p align="left">
  <a href="https://xitakse.github.io/AINativeSlide/">
    <img src="https://img.shields.io/badge/Live%20Demo-Try%20in%20Browser-4f46e5?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Live Demo" />
  </a>
  <a href="https://github.com/XitakSE/AINativeSlide/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-slate?style=for-the-badge" alt="License" />
  </a>
</p>

---

## 📖 Table of Contents
1. [Comparison with Traditional Approaches](#comparison-with-traditional-approaches)
2. [Key Features Overview](#key-features-overview)
3. [Installation Methods](#installation-methods)
4. [User Guide](#user-guide)
5. [Keyboard Shortcuts](#keyboard-shortcuts)
6. [Directory & File Structure](#directory--file-structure)
7. [License](#license)

---

## Comparison with Traditional Approaches

| Criteria | Direct PPTX Generation<br>*(python-pptx, etc.)* | Markdown Slides<br>*(Marp, etc.)* | **AINativeSlide**<br>*(HTML + Tailwind)* |
| :--- | :--- | :--- | :--- |
| **Overflow Resilience** | ❌ Frequent text clipping & overlapping | ⚠️ Vertical scroll or cut-offs | ⭕ **CSS line-clamp physically prevents overflow** |
| **Layout Expressiveness** | ❌ Rigid coordinates prone to breaking | ⚠️ Mostly bullet lists | ⭕ **Flexbox/Grid cards, matrices & pure inline SVGs** |
| **Autonomous Verification** | ❌ Tedious manual edits in PowerPoint | ⚠️ Manual Markdown adjustments | ⭕ **Python standard library tests self-heal before delivery** |
| **Paper & PDF Output** | ⚠️ Font/OS-dependent layout shifts | ⭕ PDF export supported | ⭕ **16:9 / 4:3 / A4 Landscape & Portrait zero-margin PDF** |
| **External Dependencies** | Python environment + Office software | Node.js / CLI tools | ⭕ **Zero dependencies (double-click in browser to open)** |

---

## Key Features Overview

| Category | Feature | Description |
| :--- | :--- | :--- |
| **AI Output Stability** | **Forced Overflow Prevention (`line-clamp`)** | Wraps content in `<div class="ai-content">` with strict line-clamp rules (H2: 2 lines, Body: 6 lines, Lists: 3 lines). |
| | **Autonomous Quality Testing (`verify_slide.py`)** | Zero dependencies (Pure Python 3 standard lib). Automatically validates character counts, numbering, and print CSS before delivery. |
| | **Anti-Hallucination Guardrail** | Prohibits fabricating fake terminal execution logs in CLI-less chat environments; enforces silent self-checking. |
| **Paper & Print** | **4 Aspect Ratios & Formats** | Supports 16:9 Widescreen, 4:3 Standard, **A4 Landscape (Handouts/Memos)**, and **A4 Portrait (1-Pagers)**. |
| | **Zero-Margin Print CSS (`@page`)** | Produces pixel-perfect, margin-free PDF exports directly via standard browser print (`Ctrl+P` / `Cmd+P`). |
| **Design Governance** | **Anti-AI-Smell Guardrails** | Bans equal 3-card grids, eliminates empty buzzwords, and mandates Action Titles (complete 40–60 character sentences with verbs). |
| | **6 Enterprise Wireframe Patterns** | Problem/Solution, Comparison Matrix, Scope Boundary, Architecture, Phased Workflow, and Pitfalls/FAQ. |
| | **Corporate Design Templates** | Standardizes CI colors, logo, confidential badges, and footer positioning (works with [Template-Builder](https://github.com/XitakSE/AINativeSlide-Template-Builder)). |
| | **Inline SVG Charts & Matrix Tables** | Pure inline SVG combo charts (bars & lines) and evaluation matrix tables with clear recommendation badges. |
| **AI Visuals** | **Concept Imagery Generation** | Curated prompts across 4 visual styles: Photorealistic, Manga/Comic, 3D Isometric, and Flat Vector. |
| | **Zero-Cropping Aspect Alignment** | Pre-aligns container ratios with prompt aspect ratios to eliminate unwanted CSS cropping (supports drag-and-drop replacement). |
| | **Pure Base64 Inlining** | Embeds all AI imagery and brand logos directly as Data URIs for true Single-File zero-dependency portability. |
| **Review & Present** | **Mandatory Smart Grill (Approval Gate)** | Alignment interview prior to code generation to establish outline, ratio, and image styles, eliminating cognitive drift. |
| | **Speech Script Markdown (`speech_script.md`)** | Simultaneously generates estimated timings, key takeaways, and conversational speaker notes (optional Grill choice). |
| | **In-Browser Direct Editing & Mini Toolbar** | Click to edit slide text directly with floating format bar (bold, colors, highlighter, font sizing). |
| | **Fullscreen Slideshow & Read-Only Mode** | Press **`F`** to present fullscreen, **`E`** to toggle read-only mode (prevents accidental clicks), and **`Esc`** to exit. |
| | **Batch Feedback Prompts & Auto-Save** | Aggregates per-slide notes into formatted revision prompts via **"📋 Copy Instructions"**. Background `localStorage` auto-save. |

---

## Installation Methods

AINativeSlide conforms to the open **Agent Skills specification (`SKILL.md`)**. Compatible agents—including **Codex**, **Claude Code**, **Cursor**, and **Antigravity**—will automatically recognize the skill once placed in your workspace.

### Method A: Git Clone (Recommended)
Run the following command in your workspace or project root:

```bash
git clone https://github.com/XitakSE/AINativeSlide.git .agents/skills/ainativeslide
```

### Method B: Direct ZIP Download (Restricted Networks & No Git CLI)
1. Go to the [GitHub Repository](https://github.com/XitakSE/AINativeSlide) and click **"<> Code" ➔ "Download ZIP"**.
2. Extract the archive and rename the folder to `ainativeslide`.
3. Move it to `.agents/skills/ainativeslide` in your project root (ensure `SKILL.md` is directly inside).

---

## User Guide

### 1. Slide Generation Request (Prompt Example)

Submit your topic and requirements in your AI chat:

```markdown
Please create an executive presentation using AINativeSlide (Single-File HTML format).
Do not generate code immediately; first present an outline proposal for approval (Grill interview).

[Topic]
Enterprise Modern Data Stack & Next-Gen Data Platform Strategy

[Target Audience]
C-level Executives & Board of Directors (Focus on ROI, governance, and phased rollout)

[Requirements]
1. Aspect Ratio: 16:9 Widescreen (or A4 Landscape)
2. Slide Count: 6–8 slides
3. Anti-AI-Smell Guardrails: Use complete Action Titles (verb endings) for each slide heading
4. Key Components:
   - Cover slide (CI logo & confidentiality pill)
   - AS-IS vs TO-BE architecture comparison card
   - Evaluation matrix comparing 3 approaches (highlight recommended option)
   - 4-Year ROI projection chart (Pure Inline SVG)
   - Phased rollout roadmap (4 phases)
5. Generate a speaker speech script (speech_script.md) alongside the slide HTML.
```

### 2. Autonomous Testing & Self-Healing Workflow
In agent environments, the AI automatically executes background tests and fixes any layout or numbering issues before delivering the final code.

```mermaid
flowchart LR
    A[User Prompt] --> B[AI Presents Outline Proposal (Grill)]
    B --> C{User Approval}
    C --> D[Generate HTML Code]
    D --> E[Run verify_slide.py]
    E --> F{Test Suite Passed?}
    F -- Errors Detected --> G[AI Autonomously Fixes Code]
    G --> E
    F -- Exit Code 0 --> H[🚀 Deliver Polished HTML]
```

### 3. In-Browser Review & Iteration
Open the generated HTML in Chrome, Edge, or Safari:
1. **Direct Editing**: Click any text to edit directly (automatically saved to `localStorage`). Select text to reveal the mini formatting toolbar.
2. **Slide Feedback**: Enter revision notes in the "💬 Feedback" box under any slide.
3. **Copy Instructions**: Click **"📋 Copy Instructions"** in the top toolbar, then paste the formatted instructions back into your AI chat for seamless iteration.

### 4. Presenting & Exporting to PDF
- **Fullscreen Slideshow**: Press **`F`** to launch fullscreen presentation mode (**`Esc`** to exit).
- **Save to PDF**: Click **"Save PDF"** in the toolbar (or press `Ctrl+P` / `Cmd+P`). Choose **"Save as PDF"**, set Margins to **"None"**, and check **"Background graphics"**.

---

## Keyboard Shortcuts

| Key | Mode | Description |
| :--- | :--- | :--- |
| **`F`** / **`F5`** | Edit / Present | Toggle fullscreen slideshow mode |
| **`E`** | Edit / Present | Toggle edit mode ON / OFF (Read-only mode disables text selection) |
| **`Esc`** | Present | Exit slideshow back to standard view |
| **`→` / `↓` / `Space` / `PageDown`** | Present | Advance to the next slide |
| **`←` / `↑` / `PageUp`** | Present | Return to the previous slide |
| **`Home` / `End`** | Present | Jump to the first / last slide |

*Note: Shortcuts are automatically disabled when typing in input boxes or active `contenteditable` elements.*

---

## Directory & File Structure

```
AINativeSlide/
├── AGENTS.md                # General AI coding agent instructions
├── CLAUDE.md                # Claude Code CLI entrypoint directives
├── SKILL.md                 # AI Agent Skill specification (Grill, auto-testing, patterns)
├── README.md                # Japanese documentation
├── README_EN.md             # English documentation
├── index.html               # GitHub Pages root & 16:9 interactive live showcase
├── agents/                  # Multi-Agent manifest definitions
│   └── openai.yaml          # ChatGPT / OpenAI Agent execution manifest
├── assets/                  # Agent Skills standard assets directory
│   ├── template_base.html   # Base HTML template engine optimized for AI stability
│   ├── speech_script_example.md # Speaker speech script sample document
│   └── corporate_default.html # Corporate brand design template (CI/VI compliance)
├── scripts/
│   └── verify_slide.py      # [Zero-Dependency] Pure Python 3 auto-verification & quality test tool
└── references/              # Detailed technical specifications
    ├── slide-patterns.md    # Information structuring & wireframe patterns (Anti-AI-Smell)
    ├── grill-workflow.md    # Cognitive alignment interview specification
    ├── ratio-and-print-specs.md # 16:9 / 4:3 / A4 aspect ratio & print CSS specs
    ├── ai-concept-imagery.md # Concept image generation prompt guidelines
    └── design-system.md     # Typography & robust box model specifications
```

> [!TIP]
> **💡 Pruning Unused Files for Your Target Environment**:
> This repository is pre-configured to work out-of-the-box across Google Antigravity, Claude Code, ChatGPT, Cursor, and other agent platforms. Feel free to prune files you do not need:
> - **Core Essentials**: `SKILL.md` (the primary execution contract) and `assets/` (HTML skeletons and assets)
> - **If not using ChatGPT**: You can safely delete the `agents/` directory.
> - **If not using Claude Code**: You can safely delete `CLAUDE.md`.
> - **If not using autonomous coding agents**: You can safely delete `AGENTS.md`.

*Tip: To convert and migrate your company's existing PPTX templates, use [ainativeslide-template-builder](https://github.com/XitakSE/AINativeSlide-Template-Builder).*

---

## License

MIT License © 2026 AINativeSlide Contributors. Free for commercial and personal use.
