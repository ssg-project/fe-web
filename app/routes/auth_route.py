#storage-web/app/routes/auth_route.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
import requests
import os

# 인증 블루프린트 생성
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# FastAPI 서버 URL
# FASTAPI_BASE_URL = 'http://127.0.0.1:8000/api/v1/auth'
base_url = os.getenv('SERVER_BASE_URL')

# 로그인 라우트 정의

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        api_url = f'{base_url}/user/api/v1/auth/login'
        data = {
            "email": email,
            "password": password
        }
        
        # 디버깅 로그
        print("\n=== Login Request Debug ===")
        print(f"API URL: {api_url}")
        print(f"Request Data: {data}")
        
        try:
            # API 호출
            response = requests.post(api_url, json=data)
            
            # 응답 로그
            print(f"Response Status: {response.status_code}")
            print(f"Response Body: {response.text}")
            print("==========================\n")
            
            if response.status_code == 200:  # 로그인 성공
                response_data = response.json()
                session['user_email'] = response_data['user_email']
                session['access_token'] = response_data['access_token']
                
                return redirect(url_for('main.home'))
            elif response.status_code == 401:  # 인증 실패
                error_message = response.json().get('detail', '로그인에 실패했습니다.')
                return render_template('login.html', error=error_message)
            else:
                error_message = f"오류가 발생했습니다. 상태 코드: {response.status_code}"
                return render_template('login.html', error=error_message)
                
        except requests.exceptions.RequestException as e:
            print(f"Error during API call: {e}")
            return render_template('login.html', error='서버와의 통신 중 오류가 발생했습니다.')
            
    return render_template('login.html')

# 회원가입 라우트 정의
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    # if 'user_id' in session:  # 세션이 있으면 Explorer로 이동
    #     return redirect(url_for('explorer.explorer'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        # 비밀번호 확인 로직
        if password != confirm_password:
            return render_template('signup.html', error='비밀번호가 일치하지 않습니다.')

        # API 요청 데이터 준비
        api_url = f'{base_url}/user/api/v1/auth/join'
        headers = {'Content-Type': 'application/json'}
        data = {
            "email": email,
            "password": password
        }

        try:
            # API 호출
            response = requests.post(api_url, json=data, headers=headers)

            if response.status_code == 200:  # 회원가입 성공 (200 Created)
                flash('회원가입이 완료되었습니다! 로그인하세요.', 'success')
                return redirect(url_for('auth.login'))  # 로그인 페이지로 리다이렉트
            else:
                error_message = response.json().get('detail', '회원가입에 실패했습니다.')
                return render_template('signup.html', error=error_message)

        except requests.exceptions.RequestException as e:
            print(f"Error during API call: {e}")
            return render_template('signup.html', error='서버와의 통신 중 오류가 발생했습니다.')

    return render_template('signup.html')  # GET 요청 시 회원가입 폼 렌더링

# 로그아웃 라우트 정의
@auth_bp.route('/logout', methods=['GET'])
def logout():
    if 'user_id' not in session:  # 세션이 없으면 로그인 페이지로 리다이렉트
        flash("이미 로그아웃된 상태입니다.", "info")
        return redirect(url_for('auth.login'))

    api_url = f'{base_url}/api/v1/auth/logout'

    try:
        # FastAPI 서버에 로그아웃 요청 전송 (쿠키 포함)
        response = requests.post(api_url, cookies=request.cookies)

        if response.status_code == 200:  # 로그아웃 성공
            session.clear()  # Flask 세션 삭제
            flash("로그아웃되었습니다.", "success")
            return redirect(url_for('auth.login'))
        else:
            error_message = response.json().get('detail', f"서버 로그아웃 실패 (상태 코드: {response.status_code})")
            # flash(error_message, "error")
            # return redirect(url_for('explorer.explorer'))

    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {e}")
        flash("서버와의 통신 중 오류가 발생했습니다.", "error")
        # return redirect(url_for('explorer.explorer'))

# 회원 탈퇴 라우트 정의
@auth_bp.route('/withdrawal', methods=['GET'])
def withdrawal():
    api_url = f'{base_url}/api/v1/auth/withdrawal'

    requests.post(api_url,)

# 세션 상태 확인 및 리다이렉트 라우트 정의
@auth_bp.route('/')
def check_session():
    # if 'user_id' in session:  # 세션이 있으면 Explorer로 이동
    #     return redirect(url_for('explorer.explorer'))
    # else:  # 세션이 없으면 Login으로 이동
    return redirect(url_for('auth.login'))






# #storage-web/app/routes/auth_route.py
# from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
# import requests
# import os

# # 인증 블루프린트 생성
# auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# # FastAPI 서버 URL
# # FASTAPI_BASE_URL = 'http://127.0.0.1:8000/api/v1/auth'
# base_url = os.getenv('SERVER_BASE_URL')

# # 로그인 라우트 정의

# # @auth_bp.route('/login', methods=['GET', 'POST'])
# # def login():
# #     if request.method == 'POST':
# #         email = request.form.get('email')
# #         password = request.form.get('password')
        
# #         # API 요청 데이터 준비
# #         api_url = f'{base_url}/user/api/v1/auth/login'
# #         data = {
# #             "email": email,
# #             "password": password
# #         }
        
# #         try:
# #             # API 호출 전 요청 데이터 확인
# #             print(f"Sending request to: {api_url}")
# #             print(f"Request data: {data}")
            
# #             # API 호출
# #             response = requests.post(api_url, json=data)
            
# #             # 응답 확인을 위한 출력
# #             print(f"Response status: {response.status_code}")
# #             print(f"Response body: {response.text}")
            
# #             if response.status_code == 200:  # 로그인 성공
# #                 response_data = response.json()
# #                 # 세션에 사용자 정보 저장
# #                 session['user_email'] = response_data['user_email']
# #                 session['user_id'] = str(response_data['user_id'])
# #                 session['access_token'] = response_data['access_token']
                
# #                 # 메인 페이지로 리다이렉트
# #                 return redirect(url_for('main.home'))
                
# #             elif response.status_code == 401:  # 인증 실패
# #                 error_message = response.json().get('detail', '로그인에 실패했습니다.')
# #                 return render_template('login.html', error=error_message)
                
# #             else:
# #                 error_message = f"오류가 발생했습니다. 상태 코드: {response.status_code}"
# #                 return render_template('login.html', error=error_message)
                
# #         except requests.exceptions.RequestException as e:
# #             print(f"Error during API call: {e}")
# #             return render_template('login.html', error='서버와의 통신 중 오류가 발생했습니다.')
            
# #     return render_template('login.html')



























# @auth_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     # if 'user_id' in session:  # 세션이 있으면 Explorer로 이동
#     #     return redirect(url_for('explorer.explorer'))

#     if request.method == 'POST':
#         email = request.form.get('email')  # email 필드 사용
#         password = request.form.get('password')

#         # API 요청 데이터 준비
#         api_url = f'{base_url}/user/api/v1/auth/login'
#         data = {
#             "email": email,
#             "password": password
#         }

#         try:
#             # API 호출
#             response = requests.post(api_url, json=data)

#             if response.status_code == 200:  # 로그인 성공
#                 user_email = response.json()['user_email']
#                 user_id = str(response.json()['user_id'])
                

#                 # return redirect(url_for('explorer.explorer'))  # Explorer 페이지로 리다이렉트
#                 return redirect(url_for('main.home'))


#             elif response.status_code == 401:  # 인증 실패
#                 error_message = response.json().get('detail', '로그인에 실패했습니다.')
#                 return render_template('login.html', error=error_message)
#             else:
#                 error_message = f"오류가 발생했습니다. 상태 코드: {response.status_code}"
#                 return render_template('login.html', error=error_message)

#         except requests.exceptions.RequestException as e:
#             print(f"Error during API call: {e}")
#             return render_template('login.html', error='서버와의 통신 중 오류가 발생했습니다.')

#     return render_template('login.html')  # GET 요청 시 로그인 폼 렌더링

# # 회원가입 라우트 정의
# @auth_bp.route('/signup', methods=['GET', 'POST'])
# def signup():
#     # if 'user_id' in session:  # 세션이 있으면 Explorer로 이동
#     #     return redirect(url_for('explorer.explorer'))

#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         confirm_password = request.form.get('confirm-password')

#         # 비밀번호 확인 로직
#         if password != confirm_password:
#             return render_template('signup.html', error='비밀번호가 일치하지 않습니다.')

#         # API 요청 데이터 준비
#         api_url = f'{base_url}/user/api/v1/auth/join'
#         headers = {'Content-Type': 'application/json'}
#         data = {
#             "email": email,
#             "password": password
#         }

#         try:
#             # API 호출
#             response = requests.post(api_url, json=data, headers=headers)

#             if response.status_code == 200:  # 회원가입 성공 (200 Created)
#                 flash('회원가입이 완료되었습니다! 로그인하세요.', 'success')
#                 return redirect(url_for('auth.login'))  # 로그인 페이지로 리다이렉트
#             else:
#                 error_message = response.json().get('detail', '회원가입에 실패했습니다.')
#                 return render_template('signup.html', error=error_message)

#         except requests.exceptions.RequestException as e:
#             print(f"Error during API call: {e}")
#             return render_template('signup.html', error='서버와의 통신 중 오류가 발생했습니다.')

#     return render_template('signup.html')  # GET 요청 시 회원가입 폼 렌더링

# # 로그아웃 라우트 정의
# @auth_bp.route('/logout', methods=['GET'])
# def logout():
#     if 'user_id' not in session:  # 세션이 없으면 로그인 페이지로 리다이렉트
#         flash("이미 로그아웃된 상태입니다.", "info")
#         return redirect(url_for('auth.login'))

#     api_url = f'{base_url}/user/api/v1/auth/logout'

#     try:
#         # FastAPI 서버에 로그아웃 요청 전송 (쿠키 포함)
#         response = requests.post(api_url, cookies=request.cookies)

#         if response.status_code == 200:  # 로그아웃 성공
#             session.clear()  # Flask 세션 삭제
#             flash("로그아웃되었습니다.", "success")
#             return redirect(url_for('auth.login'))
#         else:
#             error_message = response.json().get('detail', f"서버 로그아웃 실패 (상태 코드: {response.status_code})")
#             # flash(error_message, "error")
#             # return redirect(url_for('explorer.explorer'))

#     except requests.exceptions.RequestException as e:
#         print(f"Error during API call: {e}")
#         flash("서버와의 통신 중 오류가 발생했습니다.", "error")
#         # return redirect(url_for('explorer.explorer'))

# # 회원 탈퇴 라우트 정의
# @auth_bp.route('/withdrawal', methods=['GET'])
# def withdrawal():
#     api_url = f'{base_url}/user/api/v1/auth/withdrawal'

#     requests.post(api_url,)

# # 세션 상태 확인 및 리다이렉트 라우트 정의
# @auth_bp.route('/')
# def check_session():
#     # if 'user_id' in session:  # 세션이 있으면 Explorer로 이동
#     #     return redirect(url_for('explorer.explorer'))
#     # else:  # 세션이 없으면 Login으로 이동
#     return redirect(url_for('auth.login'))