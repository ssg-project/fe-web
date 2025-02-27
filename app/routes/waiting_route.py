import logging
from flask import Blueprint, request, render_template, session, redirect, url_for

# 로깅 설정
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

waiting_bp = Blueprint('waiting', __name__,
                      static_folder='static',
                      template_folder='templates')


detail_bp = Blueprint('detail', __name__,
                    static_folder='static',  # static 폴더 위치 지정
                    template_folder='templates') # templates 폴더 위치 지정

@waiting_bp.route('/waiting')
def waiting_room():
    # 요청 정보 로깅
    user_ip = request.remote_addr  # 클라이언트 IP 주소
    user_agent = request.user_agent.string  # 사용자 에이전트 (브라우저 정보 등)
    method = request.method  # 요청 메소드 (GET, POST 등)
    path = request.path  # 요청된 URL 경로

    logging.info(f'요청 정보 - IP: {user_ip}, User-Agent: {user_agent}, Method: {method}, Path: {path}')
    
    # 로그인 상태 체크
    if 'user_email' not in session:
        logging.warning(f'로그인 시도 실패 - IP: {user_ip}, User-Agent: {user_agent}')
        return redirect(url_for('auth.login'))
    
    # 대기실 페이지 로딩 시
    logging.info('대기실 페이지 로드 요청')

    try:
        return render_template('waiting.html')
    except Exception as e:
        logging.error(f"대기실 페이지 로딩 중 오류 발생: {e}")
        return f"대기실 페이지 로딩 중 오류가 발생했습니다: {e}", 500