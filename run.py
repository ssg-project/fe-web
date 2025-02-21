from app.app import create_app
# from prometheus_flask_exporter import PrometheusMetrics

app = create_app()

# metrics = PrometheusMetrics(app)

@app.get("/health")
def health_check():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
