from flask import Blueprint, request, url_for, redirect, render_template, session, jsonify, json
from flask_socketio import SocketIO, emit
import requests
import websocket
from app.config.config import SERVER_BASE_URL, WEBSOCKET_SERVER_URL


detail_bp = Blueprint('detail', __name__, 
                     static_folder='static',  # static 폴더 위치 지정
                     template_folder='templates') # templates 폴더 위치 지정



@detail_bp.route('/concert/<int:concert_id>', methods=['GET', 'POST'])
def concert_detail(concert_id):
    if 'user_email' not in session or 'access_token' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        api_url = f"{SERVER_BASE_URL}/event/api/v1/concert/{concert_id}"
        headers = {
            'Authorization': f'Bearer {session.get("access_token")}'
        }

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            concert_data = response.json().get('concert', {})
            
            return render_template('detail.html', 
                                 concert=concert_data,
                                 user_email=session.get('user_email'),
                                 config={"WEBSOCKET_SERVER_URL": WEBSOCKET_SERVER_URL})
        except requests.exceptions.RequestException as e:
            return f"API 요청 중 오류가 발생했습니다: {e}", 500

    else:
        # API 요청 URL
        api_url = f"{SERVER_BASE_URL}/ticketing/api/v1/ticket/reserve"
      
        data = {
            "concert_id": concert_id
        }

        headers = {
            'Authorization': f'Bearer {session.get("access_token")}'
        }

        try:
            # API 호출
            response = requests.post(api_url, json=data, headers=headers)
            
            # 응답 로그
            print(f"Response Status: {response.status_code}")
            print(f"Response Body: {response.text}")
            print("==========================\n")

            # websocket에 연결 성공
            if response.status_code == 200:
                try:
                    ws = websocket.create_connection(WEBSOCKET_SERVER_URL)
                    print("WebSocket connected")

                    while True:
                        message = ws.recv()  # 서버로부터 메시지 수신
                        print(f"Received message: {message}")

                        try:
                            message_data = json.loads(message)
                            print(message_data)
                            if message_data.get('type') == 'reservation_status':
                                if (message_data.get('user_id') == str(session.get('user_id')) and message_data.get('concert_id') == str(concert_id)):
                                    # 성공 처리
                                    if message_data.get('status') == 'success':
                                        print("Reservation succeeded")
                                        ws.close()
                                        # 성공 처리 로직
                                        return jsonify({
                                            "success": True, 
                                            "message": "Reservation succeeded",
                                            "redirect": url_for('payment.process_payment', concert_id=concert_id)
                                        }), 200
                                
                                    # 실패 처리
                                    elif message_data.get('status') == 'fail':
                                        print(12314)
                                        error_message = message_data.get('message', 'Reservation failed')
                                        print(f"Reservation failed: {error_message}")
                                        ws.close()
                                        # 실패 처리 로직
                                        return jsonify({"success": False, "error": error_message}), 400

                        except websocket.WebSocketException as ws_error:
                            print(f"WebSocket connection error: {ws_error}")
                            return jsonify({
                                "success": False,
                                "error": "웹소켓 연결 실패"
                            }), 500
                    
                
                except websocket.WebSocketException as ws_error:
                    print(f"WebSocket connection error: {ws_error}")
                    return jsonify({
                        "success": False,
                        "error": "웹소켓 연결 실패"
                    }), 500
            
            else:
                return jsonify({"success": False}), 400
            

            # if 데이터 확인 후 특정 데이터가 발견되면 팝업창 띄우기
            # 완료가 되면 websocket 연결 끊어주기

        except requests.exceptions.RequestException as e:
            print(f"Error during API call: {e}")
            return jsonify({"success": False}), 500
        