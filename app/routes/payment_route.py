import logging
from flask import Blueprint, render_template, session, redirect, url_for
import requests
# from config import base_url

# 로깅 설정
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/concert/<int:concert_id>/payment')
def process_payment(concert_id):
    # 요청 정보 로깅
    user_ip = request.remote_addr  # 클라이언트 IP 주소
    logging.info(f'결제 페이지 요청 - 사용자 IP: {user_ip}, 콘서트 ID: {concert_id}')

    if 'user_email' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        api_url = f"http://127.0.0.1:8003/api/v1/concert/{concert_id}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            concert = response.json()  # API 응답의 JSON 데이터를 concert 변수에 저장
            logging.info(f'API 응답 성공 - 콘서트 정보: {concert}')
            return render_template('payment.html', concert=concert)
        else:
            print(f"API 응답 에러: {response.status_code}")
            print(f"응답 내용: {response.text}")
            logging.error(f"API 응답 에러 - 상태 코드: {response.status_code}, 응답 내용: {response.text}")
            return f"콘서트 정보를 가져오는데 실패했습니다.", 400
            
    except Exception as e:
        print(f"Error details: {e}")
        logging.error(f"결제 페이지 로딩 중 오류 발생: {e}")
        return f"결제 페이지 로딩 중 오류가 발생했습니다: {e}", 500