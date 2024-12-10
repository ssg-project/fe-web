#storage-web/app/app.py
from flask import Flask, session, redirect, url_for, request
from .routes.auth_route import auth_bp
from .routes.home_route import home_bp
from .routes.explorer_route import explorer_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # 세션 암호화를 위한 비밀 키 설정

    # 블루프린트 등록
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(explorer_bp)

    return app