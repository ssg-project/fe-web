import os

# SERVER BASE URL 설정
SERVER_BASE_URL = os.getenv("SERVER_BASE_URL", "http://127.0.0.1:8000")

# Websocket 설정
WEBSOCKET_SERVER_URL = os.getenv("WEBSOCKET_URL", "ws://127.0.0.1:9000/ws")