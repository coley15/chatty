from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import time

count = 0 # Global variable

app = Flask(__name__)
socketio = SocketIO(app)

def send_updates():
    global count
    while True:
        socketio.emit('update', count)
        count += 1
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print ("A client connected")


if __name__ == '__main__':
    # use threads so the server doesn't stop when it hits time.sleep() 
    # in the send_updates function instead it can handle other requests
    update_thread = Thread(target=send_updates)
    update_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
