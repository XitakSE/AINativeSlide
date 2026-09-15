import unittest
import sys
from pathlib import Path

# パスを追加して scripts モジュールをインポート可能にする
sys.path.append(str(Path(__file__).resolve().parent.parent))
from scripts.verify_slide import SlideVerifier

class TestSlideVerifier(unittest.TestCase):
    def test_verify_valid_slide(self):
        html = '''
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <style>
            @media print {}
            @page { margin: 0; }
            .no-print {}
            </style>
        </head>
        <body class="is-editable">
            <span id="deckSlideCountText">全1スライド</span>
            <span id="deckTitleText"></span>
            <span id="deckRatioText"></span>
            <span id="toggleEditBtn"></span>
            <span id="copyCommentsBtn"></span>
            <span id="presentationModal"></span>
            <span id="selectionToolbar"></span>
            
            <script>
            function toggleEditMode() {}
            function startPresentation() {}
            function stopPresentation() {}
            function copySlideComments() {}
            function formatSelection() {}
            </script>
            
            <section class="slide" contenteditable="true">
                <h1>Test</h1>
                <div class="slide-footer">01 / 01</div>
            </section>
            
            <div class="slide-meta-box no-print">
                <span>Slide 01 / 01</span>
            </div>
        </body>
        </html>
        '''
        verifier = SlideVerifier(html, Path("dummy.html"), is_strict=True)
        verifier.check_counts()
        verifier.check_slides_content()
        verifier.check_meta_boxes()
        verifier.check_ui_components()
        verifier.check_print_css()
        
        self.assertEqual(len(verifier.errors), 0, f"Errors found: {verifier.errors}")

    def test_verify_missing_meta_box(self):
        html = '''
        <!DOCTYPE html>
        <html lang="ja">
        <body class="is-editable">
            <section class="slide" contenteditable="true">
                <h1>Test</h1>
                <div class="slide-footer">01 / 01</div>
            </section>
        </body>
        </html>
        '''
        verifier = SlideVerifier(html, Path("dummy.html"), is_strict=False)
        verifier.check_counts()
        
        self.assertGreater(len(verifier.errors), 0)
        self.assertIn('一致していません', verifier.errors[0])

    def test_carbon_anti_ai_smell_detection(self):
        html = '''
        <!DOCTYPE html>
        <html lang="ja">
        <body>
            <section class="slide" contenteditable="true">
                <div class="rounded-3xl shadow-xl bg-gradient-to-r from-purple-500 to-pink-500">
                    <h2>AI Smelly Card</h2>
                </div>
                <div class="slide-footer">01 / 01</div>
            </section>
        </body>
        </html>
        '''
        verifier = SlideVerifier(html, Path("dummy.html"), is_strict=False)
        verifier.check_slides_content()

        # Carbon 原則違反（過度な角丸、影、ネオングラデーション）の警告が3件検知されること
        warn_texts = " ".join(verifier.warnings)
        self.assertIn("過度な角丸クラス", warn_texts)
        self.assertIn("ぼやけたドロップシャドウ", warn_texts)
        self.assertIn("安易なAIネオングラデーション", warn_texts)

if __name__ == '__main__':
    unittest.main()
