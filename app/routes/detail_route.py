from flask import Blueprint, request, redirect, url_for, render_template, session
import requests
import os
from app.config.config import SERVER_BASE_URL

detail_bp = Blueprint('detail', __name__, 
                     static_folder='static',  # static 폴더 위치 지정
                     template_folder='templates') # templates 폴더 위치 지정



@detail_bp.route('/concert/<int:concert_id>', methods=['GET', 'POST'])
def concert_detail(concert_id):
    if request.method == 'GET':
        
        api_url = f"{SERVER_BASE_URL}/event/api/v1/concert/{concert_id}"

        # 헤더 설정
        headers = {
            'Authorization': f'Bearer {session.get('access_token')}'
        }
    
        try:
            # API로부터 데이터 가져오기
            response = requests.get(api_url)
            response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
            concert_data = response.json().get('concert', {})

            print("Concert Data:", concert_data)  # 데이터 구조 확인용
            
            # 데이터를 HTML에 전달
            return render_template('detail.html', concert=concert_data, email=session.get('user_email'))
        except requests.exceptions.RequestException as e:
            # 오류 발생 시 에러 메시지 반환
            return f"API 요청 중 오류가 발생했습니다: {e}", 500

    else:
        # API 요청 URL
        api_url = f"{SERVER_BASE_URL}/ticketing/api/v1/ticket/reserve"

        data = {
            "concert_id": concert_id
        }

        headers = {
            'Authorization': f'Bearer {session.get('access_token')}'
        }

        try:
            # API 호출
            response = requests.post(api_url, json=data, headers = headers)
            
            # 응답 로그
            print(f"Response Status: {response.status_code}")
            print(f"Response Body: {response.text}")
            print("==========================\n")

            # status_code = 200 일 때,
            # websocket을 연결해서 if 데이터 확인 후 특정 데이터가 발견되면 팝업창 띄우기
            # 완료가 되면 websocket 연결 끊어주기

        except requests.exceptions.RequestException as e:
            print(f"Error during API call: {e}")
            return render_template('login.html', error='서버와의 통신 중 오류가 발생했습니다.')
    
    return render_template('payment.html')


        

    
        



