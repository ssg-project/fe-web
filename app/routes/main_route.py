from flask import Blueprint, request, redirect, url_for, render_template, session
import requests
import os
from app.config.config import SERVER_BASE_URL

# 홈 페이지 블루프린트 생성
main_bp = Blueprint('main', __name__)

# FastAPI 서버 URL
# FASTAPI_BASE_URL = 'http://127.0.0.1:8000/api/v1/auth'
@main_bp.route('/home')
def home():
    try:
        # API에서 데이터 가져오기
        api_url = f'{SERVER_BASE_URL}/event/api/v1/concert/list'
        response = requests.get(api_url)
        if response.status_code == 200:
            print(session.get('user_email'))
            concert_data = response.json()
            # 역순으로 정렬
            concerts = concert_data["concerts"]
            concert_info = [
                {
                    "concert_id": concert["concert_id"],
                    "name": concert["name"],
                    "date": concert["date"],
                    "place": concert["place"],
                    "image": concert["image"]
                }
                for concert in reversed(concerts)  # reversed로 역순 정렬
            ]
        else:
            concert_info = []
            print(f"API 오류: {response.status_code}")
    except Exception as e:
        concert_info = []
        print(f"에러 발생: {str(e)}")
    
    return render_template('main.html', concert_info=concert_info)



@main_bp.route('/')
def main():
    # 로그인 여부 확인
    # if 'user_id' not in session:  # 세션에 'user' 키가 없으면 로그인 필요
    #     return redirect(url_for('auth.login'))  # 로그인 페이지로 리다이렉트
    
    # 로그인된 사용자에게만 홈 화면 표시
    return redirect(url_for('main.home'))