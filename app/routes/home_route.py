from flask import Blueprint, render_template, session, redirect, url_for

# 홈 페이지 블루프린트 생성
home_bp = Blueprint('home', __name__, url_prefix='/home')

# 홈 페이지 라우트 정의
@home_bp.route('/')
def home():
    return "home"