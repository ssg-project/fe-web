from flask import Blueprint, request, url_for, redirect, render_template, session, jsonify, json
import requests
import websocket
from app.config.config import SERVER_BASE_URL, WEBSOCKET_SERVER_URL
import logging


detail_bp = Blueprint('detail', __name__, 
                     static_folder='static',  # static 폴더 위치 지정
                     template_folder='templates') # templates 폴더 위치 지정


logger = logging.getLogger(__name__)


@detail_bp.route('/concert/<int:concert_id>', methods=['GET', 'POST'])
def concert_detail(concert_id):
    if 'user_email' not in session or 'access_token' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        api_url = f"{SERVER_BASE_URL}/event/api/v1/concert/{concert_id}"
        headers = {
            'Authorization': f'Bearer {session.get("access_token")}'
        }
        logger.info(f"detail route api - start")
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            concert_data = response.json().get('concert', {})
            logger.info(f"detail route api - success : concert_data: {concert_data}")
            
            return render_template('detail.html', 
                                 concert=concert_data,
                                 user_email=session.get('user_email'),
                                 config={"WEBSOCKET_SERVER_URL": WEBSOCKET_SERVER_URL})
        except requests.exceptions.RequestException as e:
            logger.error(f"detail route api - error: {e}")
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
            
            # websocket에 연결 성공
            if response.status_code == 200:
                try:
                    ws = websocket.create_connection(WEBSOCKET_SERVER_URL)
                    logger.info(f"detail route api websocket connection - start")

                    while True:
                        message = ws.recv()  # 서버로부터 메시지 수신
                        logger.info(f"Received message: {message}")

                        try:
                            message_data = json.loads(message)
                            logger.info(f"detail route api websocket connection - received :{message_data}")
                            if message_data.get('type') == 'reservation_status':
                                if (message_data.get('user_id') == str(session.get('user_id')) and message_data.get('concert_id') == str(concert_id)):
                                    # 성공 처리
                                    if message_data.get('status') == 'success':
                                        
                                        ws.close()
                                        logger.info(f"detail route api websocket connection - success")
                                        return jsonify({"success": True}), 200
                                
                                    # 실패 처리
                                    elif message_data.get('status') == 'fail':
                                        error_message = message_data.get('message', 'Reservation failed')
                                        ws.close()
                                        # 실패 처리 로직
                                        logger.info(f"detail route api websocket connection - Reservation failed: {error_message}")
                                        return jsonify({"success": False, "error": error_message}), 400

                        except websocket.WebSocketException as ws_error:
                            logger.info(f"WebSocket connection error 1: {ws_error}")
                            return jsonify({
                                "success": False,
                                "error": "웹소켓 연결 실패"
                            }), 500
                    
                
                except websocket.WebSocketException as ws_error:
                    logger.info(f"WebSocket connection error 2: {ws_error}")
                    return jsonify({
                        "success": False,
                        "error": "웹소켓 연결 실패"
                    }), 500
            
            else:
                logger.info(f"detail route api websocket connection - failed ")
                return jsonify({"success": False}), 400
            

            # if 데이터 확인 후 특정 데이터가 발견되면 팝업창 띄우기
            # 완료가 되면 websocket 연결 끊어주기

        except requests.exceptions.RequestException as e:
            logger.error(f"detail route api - error: {e}")
            return jsonify({"success": False}), 500
        