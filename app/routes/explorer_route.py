from flask import Blueprint, render_template, session

# Explorer 블루프린트 생성
explorer_bp = Blueprint('explorer', __name__, url_prefix='/explorer')

# Explorer 페이지 라우트 정의
@explorer_bp.route('/')
def explorer():
    if 'user' in session:  # 세션에 사용자 정보가 있는 경우만 접근 허용
        return render_template('explorer.html', username=session['user'])
    return redirect(url_for('auth.login'))  # 세션 없으면 로그인 페이지로 리다이렉트