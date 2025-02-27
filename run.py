from app.app import create_app
from prometheus_flask_exporter import PrometheusMetrics
import logging

app = create_app()

metrics = PrometheusMetrics(app)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - event-service - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)



@app.get("/health")
def health_check():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
