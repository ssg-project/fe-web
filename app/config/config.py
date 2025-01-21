from dotenv import load_dotenv
import os

load_dotenv()

# SERVER BASE URL 설정
SERVER_BASE_URL = os.getenv("SERVER_BASE_URL", "http://localhost:8000")

# Websocket 설정
WEBSOCKET_SERVER_URL = os.getenv("WEBSOCKET_URL", "ws://localhost:8080/ws")