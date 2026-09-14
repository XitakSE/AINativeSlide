#!/usr/bin/env python3
"""
AINativeSlide Automated Slide Deck Verifier & Auto-Fixer (Python 3)

外部依存なし (Pure Python 3 標準ライブラリのみ) で動作するスライド品質自動テスト＆修復ツール。
AIエージェントが生成したHTMLスライドの構造、スライド番号の連続性、
メタボックスの整合性、文字溢れ（Overflow）リスク、印刷設定を厳格に検査します。

不備がある場合は具体的な指示を出力するほか、--fix オプションを指定することで
スライド番号のズレ、メタボックスの欠落、総数カウンター、印刷CSSを決定論的に自動修復します。

使用法:
    python3 scripts/verify_slide.py <path_to_slide.html> [--strict] [--fix]
"""

import sys
import os
import re
from pathlib import Path

# アスペクト比・寸法仕様マッピング
RATIO_SPECS = {
    '16:9': {
        'slide_class': 'w-[1280px] h-[720px]',
        'meta_class': 'w-[1280px]',
        'page_css': '@page {\n      size: 16in 9in;\n      margin: 0;\n    }',
        'label_ja': '16:9 ワイド',
    },
    '4:3': {
        'slide_class': 'w-[1024px] h-[768px]',
        'meta_class': 'w-[1024px]',
        'page_css': '@page {\n      size: 4in 3in;\n      margin: 0;\n    }',
        'label_ja': '4:3 標準',
    },
    'a4_landscape': {
        'slide_class': 'w-[1188px] h-[840px]',
        'meta_class': 'w-[1188px]',
        'page_css': '@page {\n      size: A4 landscape;\n      margin: 0;\n    }',
        'label_ja': 'A4 横 (Landscape)',
    },
    'a4_portrait': {
        'slide_class': 'w-[840px] h-[1188px]',
        'meta_class': 'w-[840px]',
        'page_css': '@page {\n      size: A4 portrait;\n      margin: 0;\n    }',
        'label_ja': 'A4 縦 (Portrait)',
    }
}

class SlideFixer:
    """スライドHTML内の機械的エラーを決定論的に自動修復するクラス"""
    def __init__(self, html: str, target_file: Path):
        self.html = html
        self.target_file = target_file
        self.fix_logs = []

        self.is_corporate_template = (
            'corporate' in target_file.name.lower()
            or 'design_templates' in str(target_file)
            or '企業CI' in html
            or 'ブランドカラー定義' in html
        )

    def fix_all(self) -> tuple[str, list[str]]:
        new_html = self.html

        # 1. body の is-editable クラス修復
        new_html = self._fix_body_editable(new_html)

        # 2. スライド抽出と番号・contenteditable・比率判定
        new_html, total_slides, ratio_key = self._fix_slides(new_html)

        # 3. 印刷用 @page CSS 修復
        if ratio_key:
            new_html = self._fix_print_css(new_html, ratio_key)

        # 4. ヘッダーのカウント表示同期
        if total_slides > 0:
            new_html = self._fix_header_counter(new_html, total_slides)

        # 5. メタボックスの1:1整合性修復
        if not self.is_corporate_template and total_slides > 0:
            new_html = self._fix_meta_boxes(new_html, total_slides, ratio_key)

        return new_html, self.fix_logs

    def _fix_body_editable(self, html: str) -> str:
        body_pattern = re.compile(r'(<body[^>]*class=["\'])([^"\']*)(["\'][^>]*>)', re.IGNORECASE)
        match = body_pattern.search(html)
        if match:
            classes = match.group(2)
            if 'is-editable' not in classes.split():
                new_classes = f"{classes} is-editable".strip()
                html = body_pattern.sub(rf'\g<1>{new_classes}\g<3>', html, count=1)
                self.fix_logs.append('body 要素に "is-editable" クラスを追加しました。')
        return html

    def _fix_slides(self, html: str) -> tuple[str, int, str]:
        slide_pattern = re.compile(r'<section[^>]*class=["\'][^"\']*\bslide\b[^"\']*["\'][^>]*>[\s\S]*?</section>', re.IGNORECASE)
        matches = list(slide_pattern.finditer(html))
        total_slides = len(matches)
        if total_slides == 0:
            return html, 0, '16:9'

        # アスペクト比の判定
        first_slide = matches[0].group(0)
        ratio_key = '16:9'
        if '1024px' in first_slide and '768px' in first_slide:
            ratio_key = '4:3'
        elif '1188px' in first_slide and '840px' in first_slide:
            ratio_key = 'a4_landscape'
        elif '840px' in first_slide and '1188px' in first_slide:
            ratio_key = 'a4_portrait'

        # 後ろから置換してオフセットのズレを防止
        new_html = html
        for idx in reversed(range(total_slides)):
            slide_match = matches[idx]
            slide_num = idx + 1
            original_slide = slide_match.group(0)
            fixed_slide = self._fix_single_slide(original_slide, slide_num, total_slides)

            if fixed_slide != original_slide:
                start, end = slide_match.span()
                new_html = new_html[:start] + fixed_slide + new_html[end:]

        return new_html, total_slides, ratio_key

    def _fix_single_slide(self, slide_html: str, slide_num: int, total_slides: int) -> str:
        # 1. contenteditable="true" の保証
        if 'contenteditable' not in slide_html:
            slide_html = re.sub(r'^(<section\b)', r'\1 contenteditable="true"', slide_html, flags=re.IGNORECASE)
            self.fix_logs.append(f'Slide {slide_num}: contenteditable="true" を付与しました。')

        # 2. フッター番号表記 (XX / YY) の修復
        expected_str = f"{slide_num:02d} / {total_slides:02d}"
        page_pattern = re.compile(r'(?:>|\b)(?:Slide\s*)?0?(\d{1,2})\s*/\s*0?(\d{1,2})(?:<|\b)', re.IGNORECASE)
        match = page_pattern.search(slide_html)
        if match:
            current_detected = match.group(0).strip('<> ')
            if current_detected != expected_str:
                prefix = '>' if match.group(0).startswith('>') else ''
                suffix = '<' if match.group(0).endswith('<') else ''
                replacement = f"{prefix}{expected_str}{suffix}"
                slide_html = slide_html[:match.start()] + replacement + slide_html[match.end():]
                self.fix_logs.append(f'Slide {slide_num}: フッター番号を "{current_detected}" から "{expected_str}" に自動修正しました。')
        else:
            # フッター領域に番号を追加
            footer_pattern = re.compile(r'(<div[^>]*class=["\'][^"\']*(?:slide-footer|border-t)[^"\']*["\'][^>]*>[\s\S]*?)(</div>)', re.IGNORECASE)
            if footer_pattern.search(slide_html):
                slide_html = footer_pattern.sub(rf'\1  <div class="font-mono text-slate-500">{expected_str}</div>\n    \2', slide_html, count=1)
                self.fix_logs.append(f'Slide {slide_num}: フッター番号 "{expected_str}" を自動挿入しました。')

        return slide_html

    def _fix_print_css(self, html: str, ratio_key: str) -> str:
        spec = RATIO_SPECS.get(ratio_key, RATIO_SPECS['16:9'])
        expected_css = spec['page_css'].strip()
        page_pattern = re.compile(r'@page\s*\{[^}]*\}', re.IGNORECASE)
        if page_pattern.search(html):
            current = page_pattern.search(html).group(0)
            if current.strip() != expected_css:
                html = page_pattern.sub(expected_css, html, count=1)
                self.fix_logs.append(f'印刷用 @page CSS を比率 ({ratio_key}) に合わせて自動修復しました。')
        return html

    def _fix_header_counter(self, html: str, total_slides: int) -> str:
        counter_pattern = re.compile(r'(<span[^>]*id=["\']deckSlideCountText["\'][^>]*>).*?(</span>)', re.IGNORECASE)
        match = counter_pattern.search(html)
        if match:
            expected_counter = f"{total_slides:02d}枚"
            html = counter_pattern.sub(rf'\g<1>{expected_counter}\g<2>', html, count=1)
            self.fix_logs.append(f'ヘッダーのスライド総数表示を "{expected_counter}" に自動同期しました。')
        return html

    def _fix_meta_boxes(self, html: str, total_slides: int, ratio_key: str) -> str:
        slide_pattern = re.compile(r'(<section[^>]*class=["\'][^"\']*\bslide\b[^"\']*["\'][^>]*>[\s\S]*?</section>)', re.IGNORECASE)
        slides = list(slide_pattern.finditer(html))
        meta_pattern = re.compile(
            r'<div[^>]*class=["\'][^"\']*\bslide-meta-box\b[^"\']*["\'][^>]*>[\s\S]*?</div>(?=(?:\s*<!--[\s\S]*?-->)*\s*(?:<section\b|</main>|<div[^>]*class=["\'][^"\']*\bslide-meta-box\b|$))',
            re.IGNORECASE
        )
        meta_boxes = list(meta_pattern.finditer(html))

        if len(slides) == len(meta_boxes):
            # メタボックス内の番号のみ同期
            new_html = html
            for idx, meta_match in enumerate(meta_boxes):
                slide_num = idx + 1
                meta_html = meta_match.group(0)
                expected_meta_label = f"Slide {slide_num} / {total_slides}"
                updated_meta_html = re.sub(r'Slide\s*\d+\s*/\s*\d+', expected_meta_label, meta_html, flags=re.IGNORECASE)
                if updated_meta_html != meta_html:
                    new_html = new_html.replace(meta_html, updated_meta_html, 1)
                    self.fix_logs.append(f'メタ情報欄 {slide_num} の表示番号を "{expected_meta_label}" に同期しました。')
            return new_html

        # メタボックスが不足している場合は再生成・対配置
        spec = RATIO_SPECS.get(ratio_key, RATIO_SPECS['16:9'])
        meta_class = spec['meta_class']

        # 既存の全メタボックスを安全に一旦除去（スライド内容の巻き込みを防止）
        meta_clean_pattern = re.compile(
            r'(?:\s*<!--[^\n]*メタ情報[^\n]*-->)?\s*<div[^>]*class=["\'][^"\']*\bslide-meta-box\b[^"\']*["\'][^>]*>[\s\S]*?</div>(?=(?:\s*<!--[\s\S]*?-->)*\s*(?:<section\b|</main>|<div[^>]*class=["\'][^"\']*\bslide-meta-box\b|$))',
            re.IGNORECASE
        )
        clean_html = meta_clean_pattern.sub('', html)
        clean_html = re.sub(r'\s*<!--\s*Slide\s*\d+\s*メタ情報欄[^\n]*-->', '', clean_html, flags=re.IGNORECASE)

        # 各スライドの直下にメタボックスを挿入
        def insert_meta(match):
            nonlocal slide_idx
            slide_idx += 1
            slide_content = match.group(0)
            meta_box = f'''\n\n    <!-- Slide {slide_idx} メタ情報欄（AIへの修正指示、印刷時は非表示） -->
    <div class="slide-meta-box no-print {meta_class} mt-2 mb-8 bg-slate-900/90 backdrop-blur border border-slate-800 rounded-xl p-3.5 shadow-lg transition-colors focus-within:border-brand-500/80 focus-within:ring-1 focus-within:ring-brand-500/50">
      <div class="flex items-center justify-between pb-2 mb-2.5 border-b border-slate-800/80">
        <div class="flex items-center gap-1.5 text-xs font-semibold text-brand-300">
          <svg class="w-3.5 h-3.5 text-brand-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/></svg>
          <span class="slide-meta-title">💬 修正指示</span>
        </div>
        <span class="text-[11px] font-mono text-slate-500">Slide {slide_idx} / {total_slides}</span>
      </div>
      <div class="flex items-start gap-2.5">
        <div class="slide-comment-input flex-1 min-h-[38px] max-h-[140px] overflow-y-auto px-3 py-2 bg-slate-950/70 border border-slate-700/60 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-brand-500 leading-relaxed" contenteditable="true" data-placeholder="このスライドの修正・要望を入力（例: 箇条書きを3点から2点に集約、KPI数値を30%に変更、配色のトーンを青系に、等）"></div>
        <button onclick="clearSlideComment(this)" title="指示をクリア" class="text-slate-500 hover:text-rose-400 p-1.5 rounded hover:bg-slate-800 text-xs transition-colors shrink-0">✕</button>
      </div>
    </div>'''
            return slide_content + meta_box

        slide_idx = 0
        reconstructed_html = re.sub(
            r'<section[^>]*class=["\'][^"\']*\bslide\b[^"\']*["\'][^>]*>[\s\S]*?</section>',
            insert_meta,
            clean_html,
            flags=re.IGNORECASE
        )
        self.fix_logs.append(f'メタ情報ボックスを全スライド ({total_slides}枚) に対し1:1で自動補完・再生成しました。')
        return reconstructed_html


class SlideVerifier:
    def __init__(self, html: str, target_file: Path, is_strict: bool):
        self.html = html
        self.target_file = target_file
        self.is_strict = is_strict
        self.errors = []
        self.warnings = []

        self.is_corporate_template = (
            'corporate' in target_file.name.lower()
            or 'design_templates' in str(target_file)
            or '企業CI' in html
            or 'ブランドカラー定義' in html
        )

        self.slides = []
        self.meta_boxes = []
        self._extract_elements()

    def _extract_elements(self):
        """スライド要素とメタボックスを抽出する"""
        slide_pattern = re.compile(r'<section[^>]*class=["\'][^"\']*\bslide\b[^"\']*["\'][^>]*>([\s\S]*?)</section>', re.IGNORECASE)
        self.slides = list(slide_pattern.finditer(self.html))

        metabox_pattern = re.compile(
            r'<div[^>]*class=["\'][^"\']*\bslide-meta-box\b[^"\']*["\'][^>]*>([\s\S]*?)</div>(?=(?:\s*<!--[\s\S]*?-->)*\s*(?:<section\b|</main>|<div[^>]*class=["\'][^"\']*\bslide-meta-box\b|$))',
            re.IGNORECASE
        )
        self.meta_boxes = list(metabox_pattern.finditer(self.html))

    def run_all_checks(self):
        """すべての検証メソッドを実行する"""
        self.check_counts()
        self.check_slides_content()
        self.check_meta_boxes()
        self.check_ui_components()
        self.check_print_css()

        return self.report_results()

    def check_counts(self):
        """スライド数とメタボックス数の整合性をチェックする"""
        slide_count = len(self.slides)
        metabox_count = len(self.meta_boxes)

        if slide_count == 0:
            self.errors.append('スライド要素 (<section class="slide ...">) が1枚も見つかりません。')

        if not self.is_corporate_template:
            if slide_count > 0 and slide_count != metabox_count:
                self.errors.append(f'スライド枚数 ({slide_count}枚) とメタ情報ボックス数 ({metabox_count}個) が一致していません。各スライドの直下に必ず1つの .slide-meta-box を配置してください。')
        else:
            if metabox_count > 0 and slide_count != metabox_count:
                self.errors.append(f'デザインテンプレート内のメタ情報ボックス数 ({metabox_count}個) がスライド枚数 ({slide_count}枚) と一致していません。')

    def check_slides_content(self):
        """各スライドの内容（番号、文字数、CSSリスク、画像、Anti-AI-Smell等）を検証する"""
        slide_count = len(self.slides)

        for idx, slide in enumerate(self.slides):
            slide_num = idx + 1
            inner_html = slide.group(1)

            self._check_slide_number(slide_num, slide_count, inner_html)
            self._check_text_length(slide_num, slide.group(0), inner_html)
            self._check_css_risks(slide_num, slide.group(0), inner_html)
            self._check_images(slide_num, inner_html)
            self._check_anti_ai_smell(slide_num, inner_html)

    def _check_slide_number(self, slide_num, total_slides, inner_html):
        """フッターのスライド番号表記を検証する"""
        slide_num_str = f"{slide_num:02d}"
        expected_total_str = f"{total_slides:02d}"

        footer_exact_pattern = re.compile(rf'(?:>|\s|\b)0?{slide_num}\s*/\s*0?{total_slides}(?:<|\s|\b)', re.IGNORECASE)
        if not footer_exact_pattern.search(inner_html):
            any_number_match = re.search(r'(?:>|\s|\b)0?(\d{1,2})\s*/\s*0?(\d{1,2})(?:<|\s|\b)', inner_html)
            if any_number_match:
                detected = any_number_match.group(0).strip('<> ')
                self.errors.append(f'Slide {slide_num}: フッター番号が誤っています (検出: "{detected}" -> 正しくは "{slide_num_str} / {expected_total_str}")')
            else:
                self.errors.append(f'Slide {slide_num}: フッターのスライド番号表記 ("{slide_num_str} / {expected_total_str}") が見つかりません。')

    def _extract_plain_text(self, html_content):
        """HTMLからプレーンテキストを抽出する（文字数カウント用）"""
        text_content = html_content
        text_content = re.sub(r'<style[\s\S]*?</style>', '', text_content, flags=re.IGNORECASE)
        text_content = re.sub(r'<script[\s\S]*?</script>', '', text_content, flags=re.IGNORECASE)
        text_content = re.sub(r'<svg[\s\S]*?</svg>', '', text_content, flags=re.IGNORECASE)
        text_content = re.sub(r'<[^>]+>', ' ', text_content)
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        return text_content

    def _check_text_length(self, slide_num, slide_html, inner_html):
        """スライドのテキスト文字数が上限を超えていないかヒューリスティック検査する"""
        text_content = self._extract_plain_text(inner_html)

        is_portrait = 'h-[1188px]' in slide_html or 'h-[1123px]' in slide_html or 'portrait' in self.html.lower()
        max_chars = 1100 if is_portrait else 700
        warn_chars = 850 if is_portrait else 520

        if len(text_content) > max_chars:
            self.errors.append(f'Slide {slide_num}: 本文テキスト量が多すぎます ({len(text_content)}文字 > 上限{max_chars}文字)。枠外はみ出し防止のため要約または箇条書きを短縮してください。')
        elif len(text_content) > warn_chars:
            self.warnings.append(f'Slide {slide_num}: テキスト量が多めです ({len(text_content)}文字)。要素がスライド枠に収まっているか確認してください。')

    def _check_css_risks(self, slide_num, slide_html, inner_html):
        """見切れリスクのあるCSSや、編集機能のフェイルセーフ設定を検査する"""
        dangerous_offset_pattern = re.compile(
            r'\b(?:absolute|fixed)\b[^"\']*\b-(?:top|bottom|left|right)-\d+\b|\b-(?:mt|mb|my|top|bottom)-\d+\b',
            re.IGNORECASE
        )
        dangerous_matches = dangerous_offset_pattern.findall(inner_html)
        if dangerous_matches:
            self.errors.append(
                f'Slide {slide_num}: 枠外見切れ（Clipping）リスクのある危険な負の配置CSSが検出されました '
                f'({", ".join(set(dangerous_matches))})。'
            )

        if not self.is_corporate_template:
            slide_tag = slide_html.split('>')[0]
            if not re.search(r'\bcontenteditable=["\']true["\']|\bcontenteditable\b(?!=["\']false["\'])', slide_tag, re.IGNORECASE):
                self.errors.append(
                    f'Slide {slide_num}: スライド要素 (<section class="slide ...">) に contenteditable="true" が静的に付与されていません。'
                    f'JavaScriptランタイム未ロード時でもブラウザ標準で即座にテキスト編集できるフェイルセーフを死守するため、'
                    f'必ず contenteditable="true" を付与してください。'
                )

        if 'overflow-hidden' in inner_html:
            clipped_badges = re.findall(r'<[a-z0-9]+[^>]*class=["\'][^"\']*(?:absolute\s+[^"\']*-top-|-mt-)[^"\']*["\'][^>]*>', inner_html, re.IGNORECASE)
            if clipped_badges:
                self.errors.append(
                    f'Slide {slide_num}: 親要素の `overflow-hidden` と競合して上部が見切れるリスクのあるバッジ/要素が検出されました (検出: {len(clipped_badges)}件)。'
                    f'バッジは見出しセル内にインライン配置するか、親要素から overflow-hidden を除外して領域（pt-など）を確保してください。'
                )

        margin_percentage_hacks = re.findall(r'(?:mb|mt)-\[\d+%(?:/\d+)?\]', inner_html, re.IGNORECASE)
        if margin_percentage_hacks:
            self.errors.append(
                f'Slide {slide_num}: 脆弱なパーセンテージマージンハック ({", ".join(set(margin_percentage_hacks))}) が検出されました。'
                f'ブラウザ環境による要素の重なり（Collision）の原因となるため、決定論的なインラインSVG（viewBox）または固定Flex/Gridレイアウトで描画してください。'
            )

    def _check_images(self, slide_num, inner_html):
        """外部画像パス・URL参照の静的検査（Single-File Complete Architecture）"""
        img_src_pattern = re.compile(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\']', re.IGNORECASE)
        for img_match in img_src_pattern.finditer(inner_html):
            src_val = img_match.group(1).strip()
            if not src_val.startswith('data:image/'):
                truncated_src = src_val if len(src_val) <= 45 else src_val[:42] + '...'
                self.errors.append(
                    f'Slide {slide_num}: 外部画像参照が検出されました (src="{truncated_src}")。'
                    f'Single-File Complete Architecture（単一ファイル完結構造）を死守するため、'
                    f'画像は必ず Base64 Data URI (data:image/...;base64,...) としてインライン埋め込みしてください。'
                )

    def _check_anti_ai_smell(self, slide_num, inner_html):
        """Anti-AI-Smell ガードレール静的検査"""
        # (1) 抽象バズワード検知
        buzzword_patterns = [
            r'シナジー(?:の最大化|最大化|効果)?',
            r'シームレス(?:な連携|連携|な統合)?',
            r'DX推進(?:の加速|を加速|の実現|を目指す|を図る)',
            r'エコシステムの共創',
            r'柔軟な対応',
            r'(?:最適化|最大化|効率化|高度化|活性化|抜本的)(?:を図る|を加速|を推進|の実現|を目指す)',
        ]
        found_buzzwords = set()
        for pat in buzzword_patterns:
            for m in re.findall(pat, inner_html):
                found_buzzwords.add(m)
        for bw in sorted(found_buzzwords):
            self.warnings.append(
                f'Slide {slide_num}: 抽象的な表現 "{bw}" が検出されました (Anti-AI-Smell)。'
                f'完璧を期す必要はありませんが、現場で想起しやすい具体的アクション（「自動化」「廃止」「削減」等）や定量数値への言い換えを検討してください。'
            )

        # (2) トピック名のみ（名詞止め見出し）検知
        if slide_num > 1:
            headings = re.findall(r'<h[23][^>]*>([\s\S]*?)</h[23]>', inner_html, re.IGNORECASE)
            for h in headings:
                clean_h = re.sub(r'<[^>]+>', '', h).strip()
                if clean_h and (clean_h.endswith('について') or clean_h in ['今後の展望', '概要', 'はじめに', 'アジェンダ', 'まとめ']):
                    self.warnings.append(
                        f'Slide {slide_num}: 見出しがトピック名のみ（名詞止め: "{clean_h}"）になっています (Anti-AI-Smell)。'
                        f'ファクトと示唆・結論を含む完全な1文（Action Title: 40〜60文字）にしてください。'
                    )

        # (3) 3均等グリッドにおける視覚的アンカー検査
        if re.search(r'<div[^>]*class=["\'][^"\']*\bgrid-cols-3\b[^"\']*["\'][^>]*>', inner_html, re.IGNORECASE):
            anchor_keywords = ['CORE', '推奨', '本提案', '最重要', '必須', 'ゲート', 'Gate', '★', 'bg-brand-', 'border-brand-', 'border-2', 'scale-', 'ring-']
            has_anchor = any(k in inner_html for k in anchor_keywords)
            if not has_anchor:
                self.warnings.append(
                    f'Slide {slide_num}: 3均等グリッド (grid-cols-3) 内に視覚的アンカー（推奨案・CORE・最重要課題の強調）が見当たりません (Anti-AI-Smell)。'
                    f'無意味な均等カード化を避け、推奨案や重要要素に色枠やバッジ等のアンカーを設定してください。'
                )

    def check_meta_boxes(self):
        """メタボックス内のバッジ番号表記を検証する"""
        slide_count = len(self.slides)

        for idx, box in enumerate(self.meta_boxes):
            slide_num = idx + 1
            inner_html = box.group(1)
            expected_badge = re.compile(rf'Slide\s*0?{slide_num}\s*/\s*0?{slide_count}', re.IGNORECASE)
            if not expected_badge.search(inner_html):
                any_badge_match = re.search(r'Slide\s*0?\d+\s*/\s*0?\d+', inner_html, re.IGNORECASE)
                if any_badge_match:
                    self.errors.append(f'メタボックス {slide_num}: バッジ番号が誤っています (検出: "{any_badge_match.group(0)}" -> 正しくは "Slide {slide_num} / {slide_count}")')
                else:
                    self.warnings.append(f'メタボックス {slide_num}: バッジ表記 ("Slide {slide_num} / {slide_count}") が見つかりません。')

    def check_ui_components(self):
        """ヘッダー表記と必須コンポーネント（JSランタイム含む）の検証"""
        slide_count = len(self.slides)

        header_count_match = re.search(r'id=["\']deckSlideCountText["\'][^>]*>(.*?)</span>', self.html, re.IGNORECASE)
        if header_count_match:
            header_count_text = header_count_match.group(1).strip()
            expected_header_count = f'全{slide_count}スライド'
            if slide_count > 0 and str(slide_count) not in header_count_text:
                self.errors.append(f'ヘッダー総スライド数表記が誤っています (検出: "{header_count_text}" -> 正しくは "{expected_header_count}")')
        else:
            self.errors.append('ヘッダーに id="deckSlideCountText" の要素が見つかりません。')

        if self.is_corporate_template:
            required_ids = ['deckTitleText', 'deckRatioText', 'deckSlideCountText']
            required_js_functions = []
        else:
            required_ids = [
                'deckTitleText', 'deckRatioText', 'deckSlideCountText',
                'toggleEditBtn', 'copyCommentsBtn', 'presentationModal', 'selectionToolbar'
            ]
            required_js_functions = [
                'toggleEditMode', 'startPresentation', 'stopPresentation',
                'copySlideComments', 'formatSelection'
            ]

        for rid in required_ids:
            if not re.search(rf'id=["\']{rid}["\']', self.html, re.IGNORECASE):
                self.errors.append(f'必須要素 id="{rid}" がHTML内に存在しません。')

        for fn in required_js_functions:
            if not re.search(rf'function\s+{fn}\b', self.html, re.IGNORECASE):
                self.errors.append(f'必須JavaScript関数 {fn}() が定義されていません。')

        self._check_editability_failsafe()

    def _check_editability_failsafe(self):
        """編集機能フェイルセーフ検査 (is-editable, pointer-events)"""
        if not self.is_corporate_template:
            if not re.search(r'<body[^>]*class=["\'][^"\']*\bis-editable\b', self.html, re.IGNORECASE):
                self.errors.append(
                    'body タグに "is-editable" クラスが付与されていません (<body class="... is-editable">)。'
                    '初期ロード時の即時編集可能状態を保証するため必ず付与してください。'
                )

            if re.search(r'body:not\(\.is-editable\)[^{]*\{[^}]*pointer-events\s*:\s*none', self.html, re.IGNORECASE):
                self.errors.append(
                    'CSS内にスライドへのマウス操作を完全遮断する危険な "pointer-events: none" が検出されました。'
                    'JavaScript未ロード時やGPTのトークン省略時に編集機能が完全に死亡するため削除してください。'
                )

    def check_print_css(self):
        """印刷・PDF余白ゼロ設定の検証"""
        if not re.search(r'@page\s*\{[^}]*margin\s*:\s*0', self.html, re.IGNORECASE):
            self.errors.append('CSSに印刷用の余白ゼロ設定 (@page { margin: 0; }) が定義されていません。')

        if not re.search(r'@media\s*print', self.html, re.IGNORECASE):
            self.errors.append('印刷用メディアクエリ (@media print) が定義されていません。')

        if not re.search(r'\.no-print', self.html, re.IGNORECASE):
            self.warnings.append('印刷除外用クラス (.no-print) の定義が見当たりません。')

    def report_results(self):
        """検証結果を集計して出力し、終了コードを決定する"""
        slide_count = len(self.slides)
        metabox_count = len(self.meta_boxes)

        print('----------------------------------------------------')
        print(f'🔍 AINativeSlide スライド自動検証レポート: {self.target_file.name}')
        print(f'📊 スライド枚数: {slide_count}枚 | メタ情報ボックス: {metabox_count}個')
        print('----------------------------------------------------')

        if self.errors:
            print(f'\n❌ [TEST FAILED] {len(self.errors)}件のエラーが検出されました。\nAIは以下の指示に従って直ちにHTMLを修正してください:\n')
            for i, err in enumerate(self.errors, 1):
                print(f'  {i}. [ERROR] {err}')

        if self.warnings:
            print(f'\n⚠️ [WARNINGS] {len(self.warnings)}件の警告があります:')
            for i, warn in enumerate(self.warnings, 1):
                print(f'  {i}. [WARN] {warn}')

        if not self.errors:
            if self.warnings and self.is_strict:
                print('\n❌ [STRICT MODE FAILED] 警告が存在するため終了コード1を返します。')
                return 1
            print('\n✅ [TEST PASSED] すべての品質テストに合格しました！')
            print('   ・スライド数・番号の完全一致')
            print('   ・メタ情報ボックスの整合性')
            print('   ・文字数・はみ出しヒューリスティッククリア')
            print('   ・必須UI & 印刷用ゼロマージン設定確認済み')
            print('🚀 成果物をユーザーに納品可能です。\n')
            return 0
        else:
            return 1


def main():
    args = sys.argv[1:]
    is_strict = '--strict' in args
    is_fix = '--fix' in args
    file_args = [a for a in args if not a.startswith('--')]

    if not file_args:
        print('[USAGE] python3 scripts/verify_slide.py <path_to_html_file> [--strict] [--fix]', file=sys.stderr)
        sys.exit(2)

    target_file = Path(file_args[0]).resolve()

    if not target_file.exists():
        print(f'[ERROR] File not found: {target_file}', file=sys.stderr)
        sys.exit(2)

    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            html = f.read()
    except Exception as e:
        print(f'[ERROR] Failed to read file: {e}', file=sys.stderr)
        sys.exit(2)

    if is_fix:
        fixer = SlideFixer(html, target_file)
        fixed_html, fix_logs = fixer.fix_all()
        if fix_logs:
            print('----------------------------------------------------')
            print(f'🛠️ AINativeSlide 自動修復ログ: {target_file.name}')
            print('----------------------------------------------------')
            for log in fix_logs:
                print(f'  ✓ {log}')
            print()
            try:
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_html)
                html = fixed_html
                print(f'💾 自動修復をファイルに保存しました: {target_file.name}\n')
            except Exception as e:
                print(f'[ERROR] Failed to write fixed file: {e}', file=sys.stderr)
                sys.exit(2)
        else:
            print('ℹ️ 構造的な自動修復対象はありませんでした。\n')

    verifier = SlideVerifier(html, target_file, is_strict)
    sys.exit(verifier.run_all_checks())

if __name__ == '__main__':
    main()

