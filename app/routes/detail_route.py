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



