import os
from dotenv import load_dotenv

if not os.getenv("APP_ENV"):
    load_dotenv()

# SERVER BASE URL 설정
SERVER_BASE_URL = os.getenv("SERVER_BASE_URL")

# Websocket 설정
WEBSOCKET_SERVER_URL = os.getenv("WEBSOCKET_URL")
