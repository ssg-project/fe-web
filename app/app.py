from flask import Flask
from .routes.home_route import home_bp
from .routes.storage_route import storage_bp

def create_app():
    app = Flask(__name__)

    # 블루프린트 등록
    app.register_blueprint(home_bp)
    app.register_blueprint(storage_bp)
        
    return app