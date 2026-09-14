import unittest
import sys
from pathlib import Path

# パスを追加して scripts モジュールをインポート可能にする
sys.path.append(str(Path(__file__).resolve().parent.parent))
from scripts.assemble_deck import DeckAssembler

class TestDeckAssembler(unittest.TestCase):
    def setUp(self):
        self.template = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <title>Template</title>
    <style>@page { size: A4 portrait; margin: 0; }</style>
</head>
<body class="is-editable">
    <main class="slide-viewport">
    </main>
    <span id="deckTitleText"></span>
    <span id="deckRatioText"></span>
    <span id="deckSlideCountText"></span>
</body>
</html>'''

    def test_extract_slides(self):
        assembler = DeckAssembler(self.template, '16:9', 'ja', False)
        html_input = '''
        <section class="slide"><h1>Slide 1</h1></section>
        <div>Not a slide</div>
        <section class="slide"><h2>Slide 2</h2></section>
        '''
        slides = assembler._extract_slides(html_input)
        self.assertEqual(len(slides), 2)
        self.assertIn('Slide 1', slides[0])
        self.assertIn('Slide 2', slides[1])

    def test_assemble_basic(self):
        assembler = DeckAssembler(self.template, '16:9', 'ja', False)
        html_input = '<section class="slide"><h1>Test Title</h1></section>'
        result = assembler.assemble(html_input, 'My Test Deck')
        
        # タイトルが同期されているか
        self.assertIn('<title>My Test Deck</title>', result)
        # スライドが挿入されているか
        self.assertIn('Test Title', result)
        # メタボックスが生成されているか
        self.assertIn('slide-meta-box', result)
        # @page CSS が 16:9 用に更新されているか
        self.assertIn('size: 16in 9in;', result)

    def test_no_meta_box(self):
        assembler = DeckAssembler(self.template, '16:9', 'ja', True)
        html_input = '<section class="slide"><h1>Test Title</h1></section>'
        result = assembler.assemble(html_input)
        
        self.assertNotIn('slide-meta-box', result)

if __name__ == '__main__':
    unittest.main()
