from flask import Blueprint, request, redirect, url_for, render_template, session
import requests

# Flask 블루프린트 정의
explorer_bp = Blueprint('explorer', __name__, url_prefix='/explorer')

@explorer_bp.route('/')
def explorer():
    # Explorer 페이지 렌더링 (템플릿 파일 사용 가능)
    return render_template('explorer.html')  # 또는 "Explorer 페이지입니다."

@explorer_bp.route('/upload', methods=['POST'])
def upload_file():
    # HTML 폼에서 전달된 파일 가져오기
    files = request.files.getlist('files')  # 다중 파일 처리

    user_email = session.get('user_email')
    user_id = session.get('user_id')

    if not files:
        return "파일이 선택되지 않았습니다.", 400

    try:
        # FastAPI 서버로 파일 전송
        response = requests.post(
            'http://localhost:8000/api/v1/file/upload',  # FastAPI 서버의 업로드 엔드포인트
            files=[('files', (file.filename, file.stream, file.mimetype)) for file in files],
            cookies={'user_id': user_id, 'user_email': user_email},  # 쿠키에 user_id와 user_email 포함
        )
        if response.status_code == 200:
            return redirect(url_for('explorer.explorer'))  # 성공 시 explorer 페이지로 리다이렉트
        else:
            return f"업로드 실패: {response.text}", response.status_code
    except Exception as e:
        return f"서버 오류: {str(e)}", 500

@explorer_bp.route('/list', methods=['GET'])
def get_file_list():
    user_email = session.get('user_email')
    user_id = session.get('user_id')

    response = requests.get(
        'http://localhost:8000/api/v1/file/list',
        cookies={'user_id': user_id, 'user_email': user_email},  # 쿠키에 user_id와 user_email 포함
    ) 

    file_list = []
    if response.status_code == 200:
        file_list = response.json()['data']
    
    return render_template('explorer.html', files=file_list)
        