#!/usr/bin/env node

/**
 * AINativeSlide PDF Export CLI
 * 
 * Puppeteer（または互換ブラウザ自動化ツール）を利用して、
 * AINativeSlide HTMLファイルからヘッドレスで余白ゼロPDFを自動生成します。
 * 
 * 使用法:
 *   npx puppeteer browsers install chrome  # 初回のみ
 *   node scripts/export_pdf.js <path_to_slide.html> [output.pdf]
 * 
 * 依存:
 *   npm install puppeteer  (プロジェクトローカル or グローバル)
 * 
 * 設計思想:
 *   AIエージェントがスライドHTMLを生成した直後に本スクリプトを実行することで、
 *   人間がブラウザの印刷ダイアログを手動操作する必要なく、
 *   「AIに頼めばPDFが直接返ってくる」体験を実現します。
 */

const fs = require('fs');
const path = require('path');

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
AINativeSlide PDF Export CLI
==========================
Usage:
  node scripts/export_pdf.js <slide.html> [output.pdf] [options]

Arguments:
  <slide.html>   Path to the AINativeSlide HTML file
  [output.pdf]   Output PDF path (default: same name with .pdf extension)

Options:
  --landscape    Force landscape orientation (default: auto-detect from HTML)
  --portrait     Force portrait orientation
  --width <W>    Page width  (default: auto-detect, e.g. "16in" or "1280px")
  --height <H>   Page height (default: auto-detect, e.g. "9in" or "720px")
  --help, -h     Show this help message

Examples:
  node scripts/export_pdf.js presentation.html
  node scripts/export_pdf.js presentation.html output.pdf
  node scripts/export_pdf.js presentation.html --width 16in --height 9in
`);
    process.exit(0);
  }

  const inputPath = path.resolve(args[0]);
  if (!fs.existsSync(inputPath)) {
    console.error(`[ERROR] File not found: ${inputPath}`);
    process.exit(1);
  }

  // Determine output path
  let outputPath;
  if (args[1] && !args[1].startsWith('--')) {
    outputPath = path.resolve(args[1]);
  } else {
    outputPath = inputPath.replace(/\.html?$/i, '.pdf');
  }

  // Parse options
  let forceWidth = null;
  let forceHeight = null;
  let forceLandscape = null;

  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--landscape') forceLandscape = true;
    if (args[i] === '--portrait') forceLandscape = false;
    if (args[i] === '--width' && args[i + 1]) { forceWidth = args[++i]; }
    if (args[i] === '--height' && args[i + 1]) { forceHeight = args[++i]; }
  }

  // Attempt to load Puppeteer
  let puppeteer;
  try {
    puppeteer = require('puppeteer');
  } catch (e) {
    console.error(`[ERROR] Puppeteer is not installed.`);
    console.error(`  Install it with: npm install puppeteer`);
    console.error(`  Then run: npx puppeteer browsers install chrome`);
    process.exit(1);
  }

  console.log(`[INFO] Input:  ${inputPath}`);
  console.log(`[INFO] Output: ${outputPath}`);

  // Read HTML to auto-detect aspect ratio
  const htmlContent = fs.readFileSync(inputPath, 'utf-8');
  let pageWidth = forceWidth || '16in';
  let pageHeight = forceHeight || '9in';
  let landscape = forceLandscape !== null ? forceLandscape : true;

  // Auto-detect 4:3 vs 16:9 from @page or .slide CSS
  if (!forceWidth && !forceHeight) {
    if (htmlContent.includes('w-[1024px]') || htmlContent.includes('size: 4in 3in')) {
      pageWidth = '4in';
      pageHeight = '3in';
      console.log(`[INFO] Detected aspect ratio: 4:3 (Standard)`);
    } else {
      console.log(`[INFO] Detected aspect ratio: 16:9 (Widescreen)`);
    }
  }

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();

    // Navigate to the HTML file
    const fileUrl = `file://${inputPath}`;
    await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 30000 });

    // Wait for Tailwind CSS CDN to apply styles
    await page.waitForFunction(() => {
      return document.querySelectorAll('.slide').length > 0;
    }, { timeout: 15000 });

    // Additional wait for fonts and rendering
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Generate PDF
    await page.pdf({
      path: outputPath,
      width: pageWidth,
      height: pageHeight,
      landscape: landscape,
      printBackground: true,
      margin: { top: 0, right: 0, bottom: 0, left: 0 },
      preferCSSPageSize: true,
    });

    const stats = fs.statSync(outputPath);
    const sizeMB = (stats.size / (1024 * 1024)).toFixed(2);
    console.log(`[SUCCESS] PDF exported: ${outputPath} (${sizeMB} MB)`);

  } catch (error) {
    console.error(`[ERROR] PDF export failed: ${error.message}`);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

main().catch(err => {
  console.error(`[FATAL] ${err.message}`);
  process.exit(1);
});
