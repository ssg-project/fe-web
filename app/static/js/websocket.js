// static/js/websocket.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('booking-form');
    const websocketUrl = document.getElementById('websocket-url').value;

    form.addEventListener('submit', function(e) {
        // 웹소켓 연결
        const ws = new WebSocket(websocketUrl);
        
        ws.onopen = function() {
            console.log('WebSocket 연결됨');
        };

        ws.onmessage = function(event) {
            console.log('메시지 수신:', event.data);
            const data = JSON.parse(event.data);
            
            if (data.status === 'success') {
                alert('예매가 완료되었습니다!');
                ws.close();
            }
        };

        ws.onclose = function() {
            console.log('WebSocket 연결 종료');
        };

        ws.onerror = function(error) {
            console.error('WebSocket 에러:', error);
        };
    });
});