from flask import Blueprint, render_template, session, redirect, url_for
import requests
# from config import base_url

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/concert/<int:concert_id>/payment')
def process_payment(concert_id):
    if 'user_email' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        api_url = f"http://127.0.0.1:8003/api/v1/concert/{concert_id}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            concert = response.json()  # API 응답의 JSON 데이터를 concert 변수에 저장
            return render_template('payment.html', concert=concert)
        else:
            print(f"API 응답 에러: {response.status_code}")
            print(f"응답 내용: {response.text}")
            return f"콘서트 정보를 가져오는데 실패했습니다.", 400
            
    except Exception as e:
        print(f"Error details: {e}")
        return f"결제 페이지 로딩 중 오류가 발생했습니다: {e}", 500