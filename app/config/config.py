import os
from dotenv import load_dotenv
import json

if not os.getenv("APP_ENV"):
    load_dotenv()

SERVER_BASE_URL = os.getenv("SERVER_BASE_URL", "http://localhost:8000")
WEBSOCKET_SERVER_URL = os.getenv("WEBSOCKET_SERVER_URL", "ws://localhost:8000")

def get_secret():
    try:
        import boto3
        from botocore.exceptions import ClientError
        
        secret_name = "secret/ticketing/fe"
        region_name = "ap-northeast-2"

        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
            secret = get_secret_value_response['SecretString']
            secret_dict = json.loads(secret)
            
            return secret_dict
        except ClientError as e:
            print(f"AWS Secret Manager 접근 오류: {e}")
            return None
    except ImportError:
        print("boto3 모듈을 가져올 수 없습니다.")
        return None
    except Exception as e:
        print(f"예상치 못한 오류: {e}")
        return None

secret_data = get_secret()

if secret_data:
    try:
        SERVER_BASE_URL = secret_data["SERVER_BASE_URL"]
        WEBSOCKET_SERVER_URL = secret_data["WEBSOCKET_SERVER_URL"]
        print("AWS Secret Manager에서 설정 값을 성공적으로 가져왔습니다.")
    except KeyError as e:
        print(f"Secret Manager에서 필요한 키를 찾을 수 없습니다: {e}")
else:
    print("환경 변수에서 설정 값을 사용합니다.")