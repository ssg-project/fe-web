from flask import Blueprint, request, render_template, session, redirect, url_for

waiting_bp = Blueprint('waiting', __name__,
                      static_folder='static',
                      template_folder='templates')


detail_bp = Blueprint('detail', __name__,
                    static_folder='static',  # static 폴더 위치 지정
                    template_folder='templates') # templates 폴더 위치 지정

@waiting_bp.route('/waiting/<int:concert_id>')
def waiting_room(concert_id):
    # 로그인 상태 체크
    if 'user_email' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        return render_template('waiting.html', concert_id=concert_id)
    except Exception as e:
        return f"대기실 페이지 로딩 중 오류가 발생했습니다: {e}", 500