from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

socketio = SocketIO(app)

rooms = {}


def generate_unique_code(length):
    while True:
        code = ''
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break


@app.route('/', methods=['GET', 'POST'])
def home():
    session.clear()

    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        join = request.form.get('join', False)
        create = request.form.get('create', False)

        if not name:
            return render_template("home.html", error="Please pass a Name", code=code, name=name)

        if join != False and not code:
            return render_template("home.html", error="Please pass a Code to Join", code=code,
                                   name=name)

        room = code
        if create != False:
            generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist")

        # temporary solution to store the data in a server
        session['room'] = room
        session['name'] = name

        return redirect(url_for('room'))

    return render_template('home.html')


@app.route('/room')
def room():
    room = session.get('room')
    name = session.get('name')

    if room is None or name is None or room not in rooms:
        return redirect(url_for('home'))

    return render_template('room.html')


if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False)
