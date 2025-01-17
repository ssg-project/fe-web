from flask import Blueprint, request, redirect, url_for, render_template, session
import requests

# 홈 페이지 블루프린트 생성
main_bp = Blueprint('main', __name__)

# 홈 페이지 라우트 정의
@main_bp.route('/home')
def home():
    # API에서 데이터 가져오기
    api_url = "http://127.0.0.1:8000/api/v1/concert/list"
    response = requests.get(api_url)

    if response.status_code == 200:
        concert_data = response.json()  # JSON 응답 파싱
        # 콘서트 이름 리스트 추출
        concert_info = [
            {
                "concert_id": concert["concert_id"],
                "name": concert["name"],
                "date": concert["date"],
                "place": concert["place"]
            }
            for concert in concert_data["concerts"]
            ]
    else:
        concert_info = ["데이터를 불러올 수 없습니다."]  # 실패 시 기본 메시지

    # 콘서트 이름 리스트를 템플릿으로 전달
    return render_template('main.html', concert_info=concert_info)

@main_bp.route('/')
def main():
    # 로그인 여부 확인
    # if 'user_id' not in session:  # 세션에 'user' 키가 없으면 로그인 필요
    #     return redirect(url_for('auth.login'))  # 로그인 페이지로 리다이렉트
    
    # 로그인된 사용자에게만 홈 화면 표시
    return redirect(url_for('main.home'))