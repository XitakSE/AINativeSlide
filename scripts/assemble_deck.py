#!/usr/bin/env python3
"""
AINativeSlide Deck Assembler (Python 3)

外部依存なし (Pure Python 3 標準ライブラリのみ) で動作する決定論的スライド合成エンジン。
LLMが生成したスライドコンテンツ断片 (<section class="slide ...">) を受け取り、
ベース骨格 (assets/template_base.html) と決定論的に合体して、
アスペクト比、スライド番号 (01 / 06)、メタボックス、印刷用CSSを完全同期した
100%完全動作のSingle-File HTMLを出力します。

使用法:
    python3 scripts/assemble_deck.py <slides_snippet.html> -o my_deck.html --title "全社データ基盤刷新構想" --ratio 16:9
    cat snippets.html | python3 scripts/assemble_deck.py -o my_deck.html
"""

import sys
import os
import re
import argparse
from pathlib import Path

# アスペクト比・寸法仕様マッピング
RATIO_SPECS = {
    '16:9': {
        'slide_class': 'w-[1280px] h-[720px]',
        'meta_class': 'w-[1280px]',
        'page_css': '@page {\n      size: 16in 9in;\n      margin: 0;\n    }',
        'label_ja': '16:9 ワイド',
        'label_en': '16:9 Widescreen',
    },
    '4:3': {
        'slide_class': 'w-[1024px] h-[768px]',
        'meta_class': 'w-[1024px]',
        'page_css': '@page {\n      size: 4in 3in;\n      margin: 0;\n    }',
        'label_ja': '4:3 標準',
        'label_en': '4:3 Standard',
    },
    'a4_landscape': {
        'slide_class': 'w-[1188px] h-[840px]',
        'meta_class': 'w-[1188px]',
        'page_css': '@page {\n      size: A4 landscape;\n      margin: 0;\n    }',
        'label_ja': 'A4 横 (Landscape)',
        'label_en': 'A4 Landscape',
    },
    'a4_portrait': {
        'slide_class': 'w-[840px] h-[1188px]',
        'meta_class': 'w-[840px]',
        'page_css': '@page {\n      size: A4 portrait;\n      margin: 0;\n    }',
        'label_ja': 'A4 縦 (Portrait)',
        'label_en': 'A4 Portrait',
    }
}

# エイリアス正規化
RATIO_ALIASES = {
    '16-9': '16:9',
    'wide': '16:9',
    'widescreen': '16:9',
    '4-3': '4:3',
    'standard': '4:3',
    'a4': 'a4_landscape',
    'a4_l': 'a4_landscape',
    'a4-landscape': 'a4_landscape',
    'a4_landscape': 'a4_landscape',
    'a4-portrait': 'a4_portrait',
    'a4_p': 'a4_portrait',
    'a4_portrait': 'a4_portrait',
}

class DeckAssembler:
    def __init__(self, template_html: str, ratio_key: str = '16:9', lang: str = 'ja', no_meta_box: bool = False):
        self.template_html = template_html
        self.ratio_key = RATIO_ALIASES.get(ratio_key.lower(), '16:9')
        self.spec = RATIO_SPECS[self.ratio_key]
        self.lang = lang
        self.no_meta_box = no_meta_box

    def assemble(self, slides_input: str, title: str = '') -> str:
        """スライド断片をテンプレートに結合して完全なHTMLを生成する"""
        slides = self._extract_slides(slides_input)
        if not slides:
            raise ValueError('有効なスライド要素 (<section class="slide ...">) が入力から検出されませんでした。')

        total_slides = len(slides)

        # タイトルの推論
        if not title:
            title = self._infer_title(slides[0]) or ('スライドプレゼンテーション' if self.lang == 'ja' else 'Slide Presentation')

        # 各スライドの成形とメタボックス生成
        viewport_items = []
        for idx, slide_html in enumerate(slides):
            slide_num = idx + 1
            formatted_slide = self._format_slide(slide_html, slide_num, total_slides)
            viewport_items.append(formatted_slide)

            if not self.no_meta_box:
                meta_box = self._generate_meta_box(slide_num, total_slides)
                viewport_items.append(meta_box)

        # テンプレートへの注入
        result_html = self.template_html

        # 1. <main class="slide-viewport"> の置換
        viewport_content = '\n\n    '.join(viewport_items)
        viewport_pattern = re.compile(r'(<main[^>]*class=["\'][^"\']*\bslide-viewport\b[^"\']*["\'][^>]*>)[\s\S]*?(</main>)', re.IGNORECASE)
        if viewport_pattern.search(result_html):
            result_html = viewport_pattern.sub(rf'\1\n\n    {viewport_content}\n\n  \2', result_html, count=1)
        else:
            raise ValueError('テンプレート内に <main class="slide-viewport"> が見つかりません。')

        # 2. タイトルの同期
        result_html = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', result_html, flags=re.IGNORECASE)

        # 3. 言語タグの同期
        result_html = re.sub(r'<html[^>]*lang=["\'][^"\']*["\']', f'<html lang="{self.lang}"', result_html, flags=re.IGNORECASE)

        # 4. 印刷用 @page CSS の同期
        page_pattern = re.compile(r'@page\s*\{[^}]*\}', re.IGNORECASE)
        if page_pattern.search(result_html):
            result_html = page_pattern.sub(self.spec['page_css'].strip(), result_html, count=1)

        # 5. ヘッダーメタデータの同期
        # deckTitleText
        result_html = re.sub(
            r'(<span[^>]*id=["\']deckTitleText["\'][^>]*>).*?(</span>)',
            rf'\g<1>{title}\g<2>',
            result_html,
            flags=re.IGNORECASE
        )
        # deckRatioText
        ratio_label = self.spec['label_ja'] if self.lang == 'ja' else self.spec['label_en']
        result_html = re.sub(
            r'(<span[^>]*id=["\']deckRatioText["\'][^>]*>).*?(</span>)',
            rf'\g<1>{ratio_label}\g<2>',
            result_html,
            flags=re.IGNORECASE
        )
        # deckSlideCountText
        count_label = f"{total_slides:02d}枚" if self.lang == 'ja' else f"{total_slides:02d} Slides"
        result_html = re.sub(
            r'(<span[^>]*id=["\']deckSlideCountText["\'][^>]*>).*?(</span>)',
            rf'\g<1>{count_label}\g<2>',
            result_html,
            flags=re.IGNORECASE
        )

        return result_html

    def _extract_slides(self, html_text: str) -> list[str]:
        """HTMLテキストからスライド要素 (<section ... class="slide ...">) をすべて抽出する"""
        pattern = re.compile(r'(<section[^>]*class=["\'][^"\']*\bslide\b[^"\']*["\'][^>]*>[\s\S]*?</section>)', re.IGNORECASE)
        return pattern.findall(html_text)

    def _infer_title(self, first_slide_html: str) -> str:
        """最初のスライドからタイトルを推論する"""
        h1_match = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', first_slide_html, re.IGNORECASE)
        if h1_match:
            title = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
            if title:
                return title
        h2_match = re.search(r'<h2[^>]*>([\s\S]*?)</h2>', first_slide_html, re.IGNORECASE)
        if h2_match:
            title = re.sub(r'<[^>]+>', '', h2_match.group(1)).strip()
            # 【Lead Message】等のプレフィックスを除去
            title = re.sub(r'^[【\[].*?[】\]]\s*', '', title)
            if title:
                return title
        return ''

    def _format_slide(self, slide_html: str, slide_num: int, total_slides: int) -> str:
        """スライド要素のクラス、contenteditable属性、およびフッター番号を正規化する"""
        # 1. 開始タグの属性抽出と正規化
        tag_match = re.match(r'^<section([^>]*)>([\s\S]*)</section>$', slide_html, re.IGNORECASE)
        if not tag_match:
            return slide_html

        attrs_str = tag_match.group(1)
        inner_content = tag_match.group(2)

        # contenteditable="true" を保証
        if 'contenteditable' not in attrs_str:
            attrs_str = f' contenteditable="true"{attrs_str}'
        else:
            attrs_str = re.sub(r'contenteditable=["\'][^"\']*["\']', 'contenteditable="true"', attrs_str)

        # クラス内の幅・高さ指定を正規化
        class_match = re.search(r'class=["\']([^"\']*)["\']', attrs_str, re.IGNORECASE)
        if class_match:
            classes = class_match.group(1).split()
            # 既存の w-[...px] や h-[...px] を除去
            filtered_classes = [c for c in classes if not re.match(r'^(?:w|h)-\[\d+px\]$', c)]
            # 新しい比率クラスを追加
            filtered_classes.extend(self.spec['slide_class'].split())
            new_class_attr = f'class="{" ".join(filtered_classes)}"'
            attrs_str = re.sub(r'class=["\'][^"\']*["\']', new_class_attr, attrs_str)
        else:
            attrs_str = f' class="slide {self.spec["slide_class"]}"{attrs_str}'

        # 2. フッターのスライド番号表記 (XX / YY) を正規化
        num_str = f"{slide_num:02d}"
        total_str = f"{total_slides:02d}"

        # 既存のページ番号 (例: 01 / 01, 1 / 5, 02/06) を置換
        page_pattern = re.compile(r'(?:>|\b)(?:Slide\s*)?0?(\d{1,2})\s*/\s*0?(\d{1,2})(?:<|\b)', re.IGNORECASE)
        if page_pattern.search(inner_content):
            # タグの内外を考慮して置換
            inner_content = page_pattern.sub(rf'>{num_str} / {total_str}<' if '>' in page_pattern.search(inner_content).group(0) else f'{num_str} / {total_str}', inner_content, count=1)
        else:
            # 見つからない場合、フッター領域の末尾に番号要素を注入
            footer_pattern = re.compile(r'(<div[^>]*class=["\'][^"\']*(?:slide-footer|border-t)[^"\']*["\'][^>]*>[\s\S]*?)(</div>)', re.IGNORECASE)
            if footer_pattern.search(inner_content):
                inner_content = footer_pattern.sub(rf'\1  <div class="font-mono text-slate-500">{num_str} / {total_str}</div>\n    \2', inner_content, count=1)

        return f'<!-- Slide {slide_num} -->\n    <section{attrs_str}>{inner_content}</section>'

    def _generate_meta_box(self, slide_num: int, total_slides: int) -> str:
        """各スライド直下に配置する標準メタ情報ボックスを生成する"""
        meta_class = self.spec['meta_class']
        title_label = "💬 修正指示" if self.lang == 'ja' else "💬 Slide Instructions"
        placeholder = (
            "このスライドの修正・要望を入力（例: 箇条書きを3点から2点に集約、KPI数値を30%に変更、配色のトーンを青系に、等）"
            if self.lang == 'ja' else
            "Enter feedback or revision instructions for this slide..."
        )
        clear_label = "指示をクリア" if self.lang == 'ja' else "Clear feedback"

        return f'''<!-- Slide {slide_num} メタ情報欄（AIへの修正指示、印刷時は非表示） -->
    <div class="slide-meta-box no-print {meta_class} mt-2 mb-8 bg-slate-900/90 backdrop-blur border border-slate-800 rounded-xl p-3.5 shadow-lg transition-colors focus-within:border-brand-500/80 focus-within:ring-1 focus-within:ring-brand-500/50">
      <div class="flex items-center justify-between pb-2 mb-2.5 border-b border-slate-800/80">
        <div class="flex items-center gap-1.5 text-xs font-semibold text-brand-300">
          <svg class="w-3.5 h-3.5 text-brand-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/></svg>
          <span class="slide-meta-title">{title_label}</span>
        </div>
        <span class="text-[11px] font-mono text-slate-500">Slide {slide_num} / {total_slides}</span>
      </div>
      
      <div class="flex items-start gap-2.5">
        <div class="slide-comment-input flex-1 min-h-[38px] max-h-[140px] overflow-y-auto px-3 py-2 bg-slate-950/70 border border-slate-700/60 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-brand-500 leading-relaxed" contenteditable="true" data-placeholder="{placeholder}"></div>
        <button onclick="clearSlideComment(this)" title="{clear_label}" class="text-slate-500 hover:text-rose-400 p-1.5 rounded hover:bg-slate-800 text-xs transition-colors shrink-0">✕</button>
      </div>
    </div>'''


def main():
    parser = argparse.ArgumentParser(
        description='AINativeSlide Deck Assembler: スライド断片と骨格を決定論的に合体して完全なSingle-File HTMLを出力します。'
    )
    parser.add_argument('input_files', nargs='*', help='スライド断片HTMLファイルパス (指定がない場合は標準入力から読込)')
    parser.add_argument('-o', '--output', default='deck.html', help='出力先HTMLファイルパス (デフォルト: deck.html)')
    parser.add_argument('-t', '--template', default=None, help='ベーステンプレートHTMLパス (デフォルト: assets/template_base.html)')
    parser.add_argument('--title', default='', help='スライドデッキのタイトル (省略時はスライドから自動推論)')
    parser.add_argument('-r', '--ratio', default='16:9', choices=['16:9', '4:3', 'a4_landscape', 'a4_portrait', '16-9', '4-3', 'a4', 'a4_l', 'a4-landscape', 'a4_p', 'a4-portrait'], help='アスペクト比・用紙サイズ (デフォルト: 16:9)')
    parser.add_argument('--lang', default='ja', choices=['ja', 'en'], help='言語設定 (ja または en, デフォルト: ja)')
    parser.add_argument('--no-meta-box', action='store_true', help='メタ情報ボックスを配置しない (デザインテンプレート用)')
    parser.add_argument('--no-verify', action='store_true', help='生成後の自動品質検証 (verify_slide.py) をスキップする')

    args = parser.parse_args()

    # スクリプト自身のディレクトリからプロジェクトルートを特定
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent

    # テンプレートパスの解決
    template_path = Path(args.template) if args.template else repo_root / 'assets' / 'template_base.html'
    if not template_path.exists():
        print(f'❌ [ERROR] テンプレートファイルが見つかりません: {template_path}', file=sys.stderr)
        sys.exit(1)

    with open(template_path, 'r', encoding='utf-8') as f:
        template_html = f.read()

    # スライド入力の読み込み
    if args.input_files:
        slides_text_parts = []
        for file_path_str in args.input_files:
            fp = Path(file_path_str)
            if not fp.exists():
                print(f'❌ [ERROR] 入力ファイルが見つかりません: {fp}', file=sys.stderr)
                sys.exit(1)
            with open(fp, 'r', encoding='utf-8') as f:
                slides_text_parts.append(f.read())
        slides_input = '\n'.join(slides_text_parts)
    else:
        # 標準入力から読み込み
        if sys.stdin.isatty():
            print('⚠️ [INFO] 入力ファイルが指定されていません。スライドHTML断片を標準入力から入力してください (Ctrl+D で終了):', file=sys.stderr)
        slides_input = sys.stdin.read()

    if not slides_input.strip():
        print('❌ [ERROR] スライド入力が空です。', file=sys.stderr)
        sys.exit(1)

    try:
        assembler = DeckAssembler(
            template_html=template_html,
            ratio_key=args.ratio,
            lang=args.lang,
            no_meta_box=args.no_meta_box
        )
        final_html = assembler.assemble(slides_input, title=args.title)
    except Exception as e:
        print(f'❌ [ERROR] スライド合成中にエラーが発生しました: {e}', file=sys.stderr)
        sys.exit(1)

    # 出力ファイル書き込み
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f'✅ [SUCCESS] スライドデッキを正常に合成・出力しました: {output_path}')

    # 自動品質検証の実行
    if not args.no_verify:
        verifier_script = script_dir / 'verify_slide.py'
        if verifier_script.exists():
            print(f'\n🔍 [VERIFY] 生成されたHTMLの自動検証を実行中: {output_path}...')
            import subprocess
            res = subprocess.run([sys.executable, str(verifier_script), str(output_path)])
            if res.returncode != 0:
                print('⚠️ [WARNING] 自動検証で警告またはエラーが検出されました。', file=sys.stderr)
                sys.exit(res.returncode)

if __name__ == '__main__':
    main()
