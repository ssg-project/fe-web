from flask import Blueprint, request, redirect, url_for, render_template, session
import requests

detail_bp = Blueprint('detail', __name__, 
                     static_folder='static',  # static 폴더 위치 지정
                     template_folder='templates') # templates 폴더 위치 지정

@detail_bp.route('/concert/<int:concert_id>')
def concert_detail(concert_id):
    # API 요청 URL
    api_url = f"http://127.0.0.1:8003/api/v1/concert/{concert_id}"
    
    try:
        # API로부터 데이터 가져오기
        response = requests.get(api_url)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
        concert_data = response.json().get('concert', {})

        print("Concert Data:", concert_data)  # 데이터 구조 확인용
        
        # 데이터를 HTML에 전달
        return render_template('detail.html', concert=concert_data)
    except requests.exceptions.RequestException as e:
        # 오류 발생 시 에러 메시지 반환
        return f"API 요청 중 오류가 발생했습니다: {e}", 500



@detail_bp.route('/concert/<int:concert_id>/book')
def start_booking(concert_id):
    # 로그인 체크 - email 세션 확인
    if 'user_email' not in session:
        # next 파라미터에 원래 가려던 URL을 포함하여 리다이렉트
        return redirect(url_for('auth.login', next=f'/concert/{concert_id}/book'))
        
    try:
        # 대기실로 리다이렉트
        return redirect(url_for('waiting.waiting_room', concert_id=concert_id))
        
    except Exception as e:
        return f"예매 처리 중 오류가 발생했습니다: {e}", 500     
