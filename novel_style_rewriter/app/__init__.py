# novel_style_rewriter/app/__init__.py
from flask import Flask

def create_app():
    # Flaskアプリケーションインスタンスを作成
    app = Flask(__name__)

    # 本番環境ではDEBUGはFalseに設定
    app.config['DEBUG'] = True

    # ルートとその他のAPIエンドポイントをインポート
    from .routes import init_routes
    init_routes(app)

    return app
