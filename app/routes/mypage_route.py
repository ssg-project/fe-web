from flask import Blueprint, request, redirect, url_for, render_template, session
import requests

mypage_bp = Blueprint('mypage', __name__,
                     static_folder='static',
                     template_folder='templates')

@mypage_bp.route('/mypage')
def mypage():
    # 세션에서 사용자 정보 확인
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        # 사용자의 예매 내역 API 요청
        booking_api_url = f"http://127.0.0.1:8000/api/v1/bookings/user/{session['user_id']}"
        booking_response = requests.get(booking_api_url)
        booking_response.raise_for_status()
        booking_data = booking_response.json().get('bookings', [])
        
        # 사용자 정보 API 요청
        user_api_url = f"http://127.0.0.1:8000/api/v1/users/{session['user_id']}"
        user_response = requests.get(user_api_url)
        user_response.raise_for_status()
        user_data = user_response.json().get('user', {})
        
        return render_template('mypage.html', 
                             bookings=booking_data,
                             user=user_data)
    
    except requests.exceptions.RequestException as e:
        return f"API 요청 중 오류가 발생했습니다: {e}", 500

@mypage_bp.route('/mypage/delete', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        # 회원 탈퇴 API 요청
        withdrawal_api_url = "http://127.0.0.1:8000/api/v1/userss/withdrawal"
        
        # API 요청 데이터 준비
        delete_data = {
            "user_id": session['user_id']
        }
        
        # Authorization 헤더에 토큰 추가
        headers = {
            'Authorization': f"Bearer {session.get('access_token')}"
        }
        
        # API 호출
        response = requests.post(withdrawal_api_url, 
                               json=delete_data,
                               headers=headers)
        response.raise_for_status()
        
        # 세션 클리어
        session.clear()
        
        return redirect(url_for('main.index'))
        
    except requests.exceptions.RequestException as e:
        if hasattr(e.response, 'status_code') and e.response.status_code == 403:
            return "권한이 없습니다.", 403
        return f"회원 탈퇴 처리 중 오류가 발생했습니다: {e}", 500