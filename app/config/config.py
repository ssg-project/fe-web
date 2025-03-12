import os
from dotenv import load_dotenv
import boto3
import json
from botocore.exceptions import ClientError

if not os.getenv("APP_ENV"):
    load_dotenv()

    # SERVER BASE URL 설정
    SERVER_BASE_URL = os.getenv("SERVER_BASE_URL")

    # Websocket 설정
    WEBSOCKET_SERVER_URL = os.getenv("WEBSOCKET_SERVER_URL")

else:
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
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    
    secret_data = json.loads(secret)

    SERVER_BASE_URL = secret_data["SERVER_BASE_URL"]

    WEBSOCKET_SERVER_URL = secret_data["WEBSOCKET_SERVER_URL"]
