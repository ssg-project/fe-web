from flask import Blueprint, request, redirect, render_template, session, jsonify, json
import requests
import websocket
from app.config.config import SERVER_BASE_URL, WEBSOCKET_SERVER_URL


detail_bp = Blueprint('detail', __name__, 
                     static_folder='static',  # static 폴더 위치 지정
                     template_folder='templates') # templates 폴더 위치 지정



@detail_bp.route('/concert/<int:concert_id>', methods=['GET', 'POST'])
def concert_detail(concert_id):
    if request.method == 'GET':

        print("\n=== Session Debug in Detail ===")
        print(f"Current session email: {session.get('user_email')}")
        print(f"Current session token: {session.get('access_token')}")
        print(f"All session data: {dict(session)}")
        print("==============================\n")
        
        api_url = f"{SERVER_BASE_URL}/event/api/v1/concert/{concert_id}"

        # access_token = session.get('access_token')
        user_email = session.get('user_email')

        # 헤더 설정
        headers = {
            'Authorization': f'Bearer {session.get("access_token")}'
        }
    
        try:
            # API로부터 데이터 가져오기
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
            concert_data = response.json().get('concert', {})
            
            # API 응답 디버깅
            print("\n=== API Response Debug ===")
            print(f"Response status: {response.status_code}")
            print(f"Concert Data: {concert_data}")
            print("=========================\n")
            
            # 데이터를 HTML에 전달
            return render_template('detail.html', concert=concert_data, user_email=user_email, config={"WEBSOCKET_SERVER_URL": WEBSOCKET_SERVER_URL})
        except requests.exceptions.RequestException as e:
            # 오류 발생 시 에러 메시지 반환
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

                    response_data = response.json()

                    if "some_specific_data" in response_data:
                        ws.send(json.dumps({"type": "alert", "message": "특정 상황 발생"}))

                    ws.close()

                    return redirect(f"/concert/{concert_id}/payment")


                
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