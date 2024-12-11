from flask import Blueprint, request, redirect, url_for, render_template, session
import requests
import os

base_url = os.getenv('SERVER_BASE_URL')

# Flask 블루프린트 정의
explorer_bp = Blueprint('explorer', __name__, url_prefix='/explorer')

@explorer_bp.route('/', methods=['GET'])
def explorer():
    # 로그인 여부 확인

    user_id = request.cookies.get('user_id')  # 쿠키에서 user_id 가져오기
    user_email = request.cookies.get('user_email')  # 쿠키에서 user_email 가져오기

    if not user_id or not user_email:  # 쿠키가 없으면 로그인 필요
        return redirect(url_for('auth.login'))

    # if 'user_id' not in session:  # 세션에 'user' 키가 없으면 로그인 필요
    #     return redirect(url_for('auth.login'))  # 로그인 페이지로 리다이렉트
    user_email = session.get('user_email')
    user_id = session.get('user_id')

    response = requests.get(
        f'{base_url}/api/v1/file/list',
        cookies={'user_id': user_id, 'user_email': user_email},  # 쿠키에 user_id와 user_email 포함
    ) 

    file_list = []
    if response.status_code == 200:
        file_list = response.json()['data']
    
    return render_template('explorer.html', files=file_list)
        
@explorer_bp.route('/upload', methods=['POST'])
def upload_file():
    # 로그인 여부 확인
    if 'user_id' not in session:  # 세션에 'user' 키가 없으면 로그인 필요
        return redirect(url_for('auth.login'))  # 로그인 페이지로 리다이렉트
    # HTML 폼에서 전달된 파일 가져오기
    files = request.files.getlist('files')  # 다중 파일 처리

    user_email = session.get('user_email')
    user_id = session.get('user_id')

    if not files:
        return "파일이 선택되지 않았습니다.", 400

    try:
        # FastAPI 서버로 파일 전송
        response = requests.post(
            f'{base_url}/api/v1/file/upload',  # FastAPI 서버의 업로드 엔드포인트
            files=[('files', (file.filename, file.stream, file.mimetype)) for file in files],
            cookies={'user_id': user_id, 'user_email': user_email},  # 쿠키에 user_id와 user_email 포함
        )
        if response.status_code == 200:
            return redirect(url_for('explorer.explorer'))  # 성공 시 explorer 페이지로 리다이렉트
        else:
            return f"업로드 실패: {response.text}", response.status_code
    except Exception as e:
        return f"서버 오류: {str(e)}", 500

@explorer_bp.route('/delete', methods=['POST'])
def delete_file():
    # 로그인 여부 확인
    if 'user_id' not in session:  # 세션에 'user' 키가 없으면 로그인 필요
        return redirect(url_for('auth.login'))  # 로그인 페이지로 리다이렉트
    file_ids = request.form.getlist('file_ids')

    user_email = session.get('user_email')
    user_id = session.get('user_id')

    try:
        print("file_ids", file_ids)
        response = requests.post(
            f'{base_url}/api/v1/file/delete',  # FastAPI의 파일 삭제 엔드포인트
            json={"file_ids": file_ids},  # JSON 데이터로 파일 ID 목록 전송
            cookies={'user_id': user_id, 'user_email': user_email},
        )

        if response.status_code == 200:
            return redirect(url_for('explorer.explorer'))
        else:
            return f"삭제 실패: {response.text}", response.status_code
    except Exception as e:
        return f"서버 오류: {str(e)}", 500


@explorer_bp.route('/download', methods=['GET'])
def download_file():
    # 로그인 여부 확인
    if 'user_id' not in session:  # 세션에 'user' 키가 없으면 로그인 필요
        return redirect(url_for('auth.login'))  # 로그인 페이지로 리다이렉트
    # 파일 키를 쿼리 파라미터로 받음
    file_key = request.args.get('file_key')
    user_email = session.get('user_email')
    user_id = session.get('user_id')

    if not file_key:
        return "파일 키가 제공되지 않았습니다.", 400

    try:
        # FastAPI의 다운로드 링크 생성 API 호출
        response = requests.get(
            f'{base_url}/api/v1/file/download',
            params={'file_key': file_key},  # 파일 키를 쿼리 파라미터로 전달
            cookies={'user_id': user_id, 'user_email': user_email},
        )

        if response.status_code == 200:
            presigned_url = response.json().get("url")
            if presigned_url:
                return redirect(presigned_url)  # Presigned URL로 리다이렉트
            else:
                return "다운로드 링크 생성 실패", 400
        else:
            return f"FastAPI 오류: {response.text}", response.status_code
    except Exception as e:
        return f"서버 오류: {str(e)}", 500