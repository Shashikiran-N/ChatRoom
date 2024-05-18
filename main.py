from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, join_room, leave_room, send
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False)
