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
   - [1. Fullscreen Presentation Mode (Slideshow)](#1-fullscreen-presentation-mode-slideshow)
   - [2. Speaker Notes](#2-speaker-notes)
   - [3. Table of Contents & Slide Index (TOC Drawer)](#3-table-of-contents--slide-index-toc-drawer)
   - [4. In-Browser Direct Text Editing & Floating Formatting Bar](#4-in-browser-direct-text-editing--floating-formatting-bar)
   - [5. Theme Color Presets & Global Font Scaling](#5-theme-color-presets--global-font-scaling)
   - [6. Per-Slide Feedback Comments & AI Iteration Loop](#6-per-slide-feedback-comments--ai-iteration-loop)
   - [7. AI Concept Imagery & Drag-and-Drop Image Replacement](#7-ai-concept-imagery--drag-and-drop-image-replacement)
   - [8. Strict Aspect Ratio Control (16:9 / 4:3) & Zero-Margin PDF Print](#8-strict-aspect-ratio-control-169--43--zero-margin-pdf-print)
3. [Keyboard Shortcuts](#keyboard-shortcuts)
4. [Directory & File Structure](#directory--file-structure)
5. [User Guide: Working with AI (ChatGPT, Claude, Gemini, Cursor, etc.)](#user-guide-working-with-ai)
6. [🚀 Future Roadmap](#-future-roadmap)

---

## Philosophy & Key Advantages

Traditional presentation tools often suffer from font discrepancies across devices, expensive license requirements, collaboration conflicts, and inconsistent styling. NativeSlide solves these issues by building entirely on open Web standards (HTML5 + Tailwind CSS CDN + Google Fonts + Vanilla JS).

- **100% Self-Contained Single-File HTML**: No Node.js, npm, bundlers, or local servers required. Simply double-click to open in any modern browser, edit directly, and present instantly.
- **Modern Executive Aesthetics**: Pre-configured with balanced Tailwind color palettes, crisp typography (Plus Jakarta Sans & Noto Sans JP), and structured card layouts.
- **Seamless AI Iteration**: Features dedicated per-slide feedback inputs and a one-click copy button that formats your notes into structured prompt instructions ready for any LLM (ChatGPT, Claude, Gemini, Cursor, etc.).

---

## Implemented Features

### 1. Fullscreen Presentation Mode (Slideshow)
Press the **"▶ Present"** button in the header or hit **`F`** on your keyboard to launch presentation mode.
- **Smart Aspect-Ratio Auto-Fit**: Uses CSS `transform: scale()` to dynamically center and maximize slides to fill any display resolution while strictly preserving the aspect ratio (16:9 or 4:3).
- **Smooth Navigation**:
  - `→` / `↓` / `Space` / `PageDown` / Click right side: Next slide
  - `←` / `↑` / `PageUp` / Click left side: Previous slide
- **Laser Pointer (`L` key)**: Replaces the cursor with a glowing red laser dot for highlighting key points.
- **Instant Exit (`Esc` key)**: Quickly return to the standard editing mode at any time.

### 2. Speaker Notes
Each slide includes a tabbed metadata box positioned directly below the canvas.
- **During Preparation & Editing**: Click the **"🎤 Speaker Notes"** tab to draft talking points and presenter scripts (`contenteditable="true"`).
- **During Live Presentation**: Press **`N`** to toggle a translucent dark overlay displaying your speaker notes for the current slide.
- **Print-Safe**: Speaker notes and feedback panels are automatically hidden when printing or exporting to PDF via `@media print`.

### 3. Table of Contents & Slide Index (TOC Drawer)
Click the **"☰ Menu"** button on the top-left to slide out a smooth drawer navigation.
- **Automatic Heading Detection**: Dynamically scans `h1` and `h2` headings across all slides to generate titles and slide numbers.
- **One-Click Jump**: Click any title to jump directly to that slide (scrolls in edit mode, switches instantly in presentation mode).

### 4. In-Browser Direct Text Editing & Floating Formatting Bar
- **Direct Editing**: Click any text element on the slide to edit it immediately.
- **Floating Mini Toolbar**: Selecting text automatically reveals a floating format bar above the selection:
  - **Bold**
  - **Font Size Adjustment**: Fine-tune selected text with `[A-]` and `[A+]`
  - **Color Picker**: Apply brand theme accent colors to specific words
  - **Highlighter**: Yellow and green marker effects for highlighting keywords
  - **Clear Formatting**: Reset inline styles with a single click

### 5. Theme Color Presets & Global Font Scaling
- **One-Click Palette Switch**: Choose from 5 curated corporate themes (Indigo, Navy, Emerald, Amber, Rose) or pick a custom hex color with the native color picker.
- **Global Typography Scaling**: Scale font sizes across all slides from 85% to 125% using the header `[A-]` `100%` `[A+]` controller.

### 6. Per-Slide Feedback Comments & AI Iteration Loop
- Enter specific change requests into the **"💬 Feedback"** tab under any slide (e.g., "Shorten this bullet point", "Wrap text cleanly", "Update quarterly metrics").
- **"📋 Copy Instructions"**: Automatically formats all comments across slides into an organized prompt and copies it to your clipboard. Paste it directly into your AI chat to request the updated HTML.
- **"📥 Save HTML"**: Download the current HTML with all your edits and comments preserved.

### 7. AI Concept Imagery & Drag-and-Drop Image Replacement
- Pre-configured prompt templates for AI image generators (DALL-E 3, Midjourney, Imagen) tailored for abstract business concepts (system architectures, pipelines, data unifications) without garbled text.
- Drag-and-drop any image from your desktop directly onto a slide's `.image-dropzone` to instantly replace it.

### 8. Strict Aspect Ratio Control (16:9 / 4:3) & Zero-Margin PDF Print
- Designed with `@page { size: 16in 9in; margin: 0; }` and `.slide { page-break-inside: avoid; }` to produce pixel-perfect, margin-free PDF exports using your browser's Print dialog ("Save as PDF").

### 9. Buttonless Automatic Language Adaptation
To prevent UI clutter and keep the toolbar minimal and focused, there are no manual language switch buttons.
- **Japanese Prompts**: The AI generates slides with `<html lang="ja">`, creating Japanese headings, content, and annotations.
- **Non-Japanese Prompts (English, etc.)**: The AI generates slides with `<html lang="en">`. The embedded JavaScript silently and automatically localizes all UI controls (Menu, Copy Feedback, Save HTML, Present, Save PDF), TOC drawer (Table of Contents), meta box tabs (Feedback, Speaker Notes), input placeholders, and AI revision copy formats (`【Slide X Feedback】`) into clean English.

---

## Keyboard Shortcuts

| Key | Mode | Action |
| :--- | :--- | :--- |
| **`F`** / **`F5`** | Edit / Present | Start / Stop fullscreen presentation mode |
| **`Esc`** | Present / Drawer | Exit presentation mode or close TOC drawer |
| **`→`** / **`↓`** / **`Space`** / **`PageDown`** | Present | Next slide |
| **`←`** / **`↑`** / **`PageUp`** | Present | Previous slide |
| **`N`** | Present | Toggle speaker notes overlay |
| **`L`** | Present | Toggle red laser pointer mode |

*Note: Shortcuts are automatically disabled when typing in input boxes or active `contenteditable` elements to prevent interference.*

---

## Directory & File Structure

```
NativeSlide/
├── SKILL.md                 # AI Agent Skill specification
├── README.md                # Japanese documentation
├── README_EN.md             # English documentation
├── references/              # Detailed specifications & guidelines
│   ├── grill-workflow.md    # Cognitive alignment interview specification
│   ├── ratio-and-print-specs.md # 16:9 / 4:3 aspect ratio & print CSS specs
│   ├── ai-concept-imagery.md # Concept image generation prompt guidelines
│   ├── design-system.md     # Typography & robust card box model specs
│   ├── slide-patterns.md    # Reusable slide layout patterns
│   └── vision-reverse-engineering.md # Reverse-engineering image slides into HTML
├── resources/               # Universal base HTML template
│   └── template_base.html
└── examples/                # Complete interactive slide examples
    ├── slide_16_9_example.html     (16:9 Japanese sample)
    ├── slide_16_9_en_example.html  (16:9 English sample)
    └── slide_4_3_example.html      (4:3 Japanese sample)
```

---

## User Guide: Working with AI

1. **Send Slide Request**:
   - Provide your topic, audience, and key messages to your AI assistant (ChatGPT, Claude, Gemini, Cursor, Copilot, etc.).
2. **Answer the 4 Grill Questions**:
   - The AI will confirm your Target Audience, Aspect Ratio (16:9 or 4:3), Slide Count, and Image Needs. Respond simply with the option numbers (e.g., `1-A, 2-A, 3-B, 4-B`).
3. **Save and Open HTML**:
   - Save the generated code as `presentation.html` and open it in Google Chrome, Microsoft Edge, or Safari.
4. **Refine in Browser & Iterate with AI**:
   - Edit text directly, adjust theme colors, and type revision requests into the "💬 Feedback" tabs below each slide.
   - Click "Copy Instructions" to copy all feedback and send it back to the AI for instant revision.
5. **Present & Export to PDF**:
   - Press **`F`** to present full-screen, using **`N`** for speaker notes and **`L`** for the laser pointer.
   - Click "Save PDF" in the toolbar with margins set to "None" and background graphics "Enabled" for clean PDF distribution.

---

## 🚀 Future Roadmap

- [ ] **Slide Manager UI**: Drag-and-drop slide reordering, duplicating, deleting, and one-click pattern insertion.
- [ ] **Business Charts (SVG / Chart.js)**: Native inline bar, line, and doughnut charts dynamically synchronized with theme colors.
- [ ] **Intuitive Table Editor**: One-click row/column additions and cell highlight toggles.
- [ ] **Corporate Branding & Confidentiality Badges**: Global corporate logo insertion and confidentiality status toggles (`CONFIDENTIAL`, `INTERNAL ONLY`, `PUBLIC`).
- [ ] **Vector Icon Library**: Built-in searchable icon picker (Lucide / Heroicons).
- [ ] **Presentation Timer & Pacing Alerts**: Live elapsed time and remaining time progress bar for conference talks.

---

## License

MIT License © 2026 NativeSlide Contributors. Free for commercial and personal use.
