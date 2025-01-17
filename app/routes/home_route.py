#storage-web/app/routes/home_route.py
from flask import Blueprint, render_template, session, redirect, url_for


# home_bp를 유지하고 경로만 수정
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('main.html')

# 홈 페이지 라우트 정의
# @home_bp.route('/')
# def home():
#     # 로그인 여부 확인
#     if 'user_id' not in session:  # 세션에 'user' 키가 없으면 로그인 필요
#         return redirect(url_for('auth.login'))  # 로그인 페이지로 리다이렉트
    
#     # 로그인된 사용자에게만 홈 화면 표시
#     # return redirect(url_for('explorer.explorer'))