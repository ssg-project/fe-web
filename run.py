from app.app import create_app
from flask_socketio import SocketIO

app = create_app()
socketio = SocketIO(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)