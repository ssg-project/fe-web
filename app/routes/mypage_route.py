from flask import Blueprint, request, redirect, url_for, render_template, session
import requests

mypage_bp = Blueprint('mypage', __name__,
                     static_folder='static',
                     template_folder='templates')

@mypage_bp.route('/mypage')
def mypage():
    # 세션에서 사용자 정보 확인
    if 'user_email' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        # 세션에서 이메일 정보 가져오기
        user_email = session.get('user_email')
        
        return render_template('mypage.html', 
                             user_email=user_email)
    
    except Exception as e:
        print(f"Error: {e}")
        return "오류가 발생했습니다.", 500

@mypage_bp.route('/mypage/delete', methods=['POST'])
def delete_account():
    if 'user_email' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        # 회원 탈퇴 API 요청
        withdrawal_api_url = "http://127.0.0.1:8000/user/api/v1/userss/withdrawal"
        
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
        
        return redirect(url_for('main.home'))
        
    except requests.exceptions.RequestException as e:
        if hasattr(e.response, 'status_code') and e.response.status_code == 403:
            return "권한이 없습니다.", 403
        return f"회원 탈퇴 처리 중 오류가 발생했습니다: {e}", 500


@mypage_bp.route('/mypage/tickets')
def tickets():
    # 로그인 체크
    if 'user_email' not in session:
        return redirect(url_for('auth.login'))
        
    try:
        # API에서 예매 내역 가져오기
        # api_url = f'{base_url}/api/v1/bookings'
        # response = requests.get(api_url, cookies=request.cookies)
        # tickets_data = response.json()
        
        # 임시 데이터
        tickets_data = {
            "tickets": [
                {
                    "concert_name": "2024 봄 콘서트",
                    "concert_date": "2024-03-15",
                    "venue": "서울공연장",
                    "seat": "A-15",
                    "status": "예매완료"
                }
            ]
        }
        
        return render_template('tickets.html', tickets=tickets_data['tickets'])
                             
    except Exception as e:
        print(f"Error fetching tickets: {e}")
        return "예매 내역을 불러오는 중 오류가 발생했습니다.", 500