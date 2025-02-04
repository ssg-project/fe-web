from app.app import create_app

@app.get("/health")
async def health_check():
    return {"status": "ok"}, 200

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
