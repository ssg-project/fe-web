#storage-web/app/routes/auth_route.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
import requests
from app.config.config import SERVER_BASE_URL
import logging



logger = logging.getLogger("web-fe")

# 인증 블루프린트 생성
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# 로그인 라우트 정의
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        api_url = f'{SERVER_BASE_URL}/user/api/v1/auth/login'
        data = {
            "email": email,
            "password": password
        }

        logger.info(f"auth route login api - start : API URL: {api_url}, email: {data}")
        
        try:
            # API 호출
            response = requests.post(api_url, json=data)
                       
            if response.status_code == 200:  # 로그인 성공
                response_data = response.json()

                
                session.clear()  # 기존 세션 제거
                session.permanent = True  # 세션 영구 설정

                session['user_id'] = response_data['user_id']
                session['user_email'] = response_data['user_email']
                session['access_token'] = response_data['access_token']


                session.modified = True  # 세션 변경 사항 명시적 저장

                next_page = request.args.get('next')
                response = make_response(redirect(next_page if next_page else url_for('waiting.waiting_room')))

                # 세션 쿠키 설정
                max_age = 3600  # 1시간
                response.set_cookie(
                    'session',
                    session.get('user_email'),
                    max_age=max_age,
                    httponly=True,
                    secure=False,  # 개발환경에서는 False
                    samesite='Lax'
                )
                logger.info(f"auth route login api - success")
                return response


            elif response.status_code == 401:
                error_message = response.json().get('detail', '로그인에 실패했습니다.')
                return render_template('login.html', error=error_message)
            else:
                error_message = f"오류가 발생했습니다. 상태 코드: {response.status_code}"
                return render_template('login.html', error=error_message)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"auth route login api - error: {e}")
            return render_template('login.html', error='서버와의 통신 중 오류가 발생했습니다.')
            
    return render_template('login.html')

# 회원가입 라우트 정의
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        # 비밀번호 확인 로직
        if password != confirm_password:
            return render_template('signup.html', error='비밀번호가 일치하지 않습니다.')

        # API 요청 데이터 준비
        api_url = f'{SERVER_BASE_URL}/user/api/v1/auth/join'
        headers = {'Content-Type': 'application/json'}
        data = {
            "email": email,
            "password": password
        }

        try:
            # API 호출
            response = requests.post(api_url, json=data, headers=headers)
            logger.info(f"auth route join api - start : API URL: {api_url}, Request Data: {data}")
            if response.status_code == 200:  # 회원가입 성공 (200 Created)
                flash('회원가입이 완료되었습니다! 로그인하세요.', 'success')
                logger.info(f"auth route join api - success")
                return redirect(url_for('auth.login'))  # 로그인 페이지로 리다이렉트
            else:
                error_message = response.json().get('detail', '회원가입에 실패했습니다.')
                return render_template('signup.html', error=error_message)

        except requests.exceptions.RequestException as e:
            print(f"Error during API call: {e}")
            logger.error(f"auth route join api - error: {e}")
            return render_template('signup.html', error='서버와의 통신 중 오류가 발생했습니다.')

    return render_template('signup.html')  # GET 요청 시 회원가입 폼 렌더링

# 로그아웃 라우트 정의
@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    print("Logout started. Current session:", dict(session))
    
    # 토큰이 없으면 바로 로그아웃 처리
    access_token = session.get('access_token')
    if not access_token:
        session.clear()
        flash("로그아웃되었습니다.", "success")
        return redirect(url_for('auth.login'))
    
    # API 로그아웃 요청
    api_url = f'{SERVER_BASE_URL}/user/api/v1/auth/logout'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    try:
        # API 호출
        response = requests.post(api_url, headers=headers)
        logger.info(f"auth route logout api - start : API URL: {api_url}, access_token: {access_token}")
        
        # 세션 정리
        session.clear()
        
        # 세션 쿠키 만료 처리
        response = make_response(redirect(url_for('auth.login')))
        response.set_cookie('session', '', expires=0)
        
        flash("로그아웃되었습니다.", "success")
        logger.info(f"auth route logout api - success")
        return response
        
    except requests.exceptions.RequestException as e:

        flash("로그아웃 중 오류가 발생했습니다.", "error")
        # 에러 발생해도 세션은 클리어
        session.clear()
        logger.error(f"auth route logout api - error: {e}")
        return redirect(url_for('auth.login'))

# 회원 탈퇴 라우트 정의
@auth_bp.route('/withdrawal', methods=['GET'])
def withdrawal():
    api_url = f'{SERVER_BASE_URL}/api/v1/auth/withdrawal'

    requests.post(api_url,)

# 세션 상태 확인 및 리다이렉트 라우트 정의
@auth_bp.route('/')
def check_session():
    # if 'user_id' in session:  # 세션이 있으면 Explorer로 이동
    #     return redirect(url_for('explorer.explorer'))
    # else:  # 세션이 없으면 Login으로 이동
    return redirect(url_for('auth.login'))
