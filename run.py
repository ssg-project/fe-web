from app.app import create_app
from prometheus_flask_exporter import PrometheusMetrics
import logging
import os


# Kubernetes 환경에서 파드 및 노드 정보 가져오기
pod_name = os.environ.get("POD_NAME", "unknown-pod")
node_name = os.environ.get("NODE_NAME", "unknown-node")


logger = logging.getLogger("web-fe")
logger.setLevel(logging.INFO)

# 중복 핸들러 방지
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s "
        f"{{pod: {pod_name}, node: {node_name}}}"  # pod_name, node_name 직접 추가
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

app = create_app()

metrics = PrometheusMetrics(app)



@app.get("/health")
def health_check():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)
