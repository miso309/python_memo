# novel_style_rewriter/app/routes.py
from flask import request, jsonify
from .utils import preprocess_text
from model.model import TextRewriterModel

# モデルインスタンスの生成（ここではダミーとして簡略化しています）
model = TextRewriterModel(vocab_size=10000, embedding_dim=256, hidden_dim=512)

def init_routes(app):
    @app.route('/')
    def home():
        return "Welcome to the Novel Style Rewriter!"

    @app.route('/rewrite', methods=['POST'])
    def rewrite():
        # ユーザー入力を取得
        input_text = request.form.get('text', '')

        # 入力テキストを前処理
        processed_text = preprocess_text(input_text)

        # モデルを使用してテキストをリライト
        # ここでは実際にはモデルの入出力処理が必要ですが、例示のために省略します
        output_text = "Rewritten text based on the author's style."

        # JSON形式で結果を返す
        return jsonify({
            'original': input_text,
            'rewritten': output_text
        })
