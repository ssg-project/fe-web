#storage-web/app/app.py
from flask import Flask, session, redirect, url_for, request
from .routes.auth_route import auth_bp
from .routes.main_route import main_bp
from .routes.detail_route import detail_bp
from .routes.waiting_route import waiting_bp
from .routes.mypage_route import mypage_bp
from .routes.payment_route import payment_bp
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # 세션 암호화를 위한 비밀 키 설정

    app.config.update(
        SESSION_COOKIE_NAME='session',
        SESSION_COOKIE_HTTPONLY=True,  # 쿠키를 자바스크립트에서 접근할 수 없게 설정
        SESSION_COOKIE_SECURE=False,  # HTTPS에서만 쿠키 전송
        # SESSION_COOKIE_SAMESITE='Lax',  # SameSite 설정 (크로스 사이트 쿠키 전송 허용)
        PERMANENT_SESSION_LIFETIME=timedelta(hours=1)

    )
    
    # 블루프린트 등록
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(detail_bp)
    app.register_blueprint(waiting_bp)
    app.register_blueprint(mypage_bp)
    app.register_blueprint(payment_bp)
    return app