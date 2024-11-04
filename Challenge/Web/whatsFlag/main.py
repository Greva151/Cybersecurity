import os
from uuid import uuid4

from flask import Flask, jsonify, session, render_template, request, g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or str(uuid4())
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

db.init_app(app)

admin_chat_uuid = None

class Message(db.Model):
    uuid = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()))
    text = db.Column(db.String)
    chat_uuid = db.Column(db.String, db.ForeignKey('chat.uuid'))


user_chat = db.Table(
    'user_chat',
    db.Column('chat_uuid', db.String, db.ForeignKey('chat.uuid')),
    db.Column('user_uuid', db.String, db.ForeignKey('user.uuid'))
)


class Chat(db.Model):
    uuid = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()))
    invite = db.Column(db.String, unique=True, default=lambda: str(uuid4()))
    messages = db.relationship('Message', backref='chat')


class User(db.Model):
    uuid = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()))
    chats = db.relationship('Chat', secondary=user_chat, backref='users')

    def chat_allowed(self, chat: Chat):
        for c in self.chats:
            if c.uuid == chat.uuid:
                return True

        return False


@app.before_request
def ensure_uuid():
    user = None
    if 'user' in session:
        user = db.session.get(User, session['user'])

    if not user:
        user = User()
        db.session.add(user)
        db.session.commit()
        session['user'] = user.uuid


@app.route('/')
def index():
    return render_template('index.html', admin_chat=admin_chat_uuid)


@app.get('/chats')
def get_chats():
    user = db.get_or_404(User, session['user'])
    return jsonify(list(map(lambda x: x.uuid, user.chats)))


@app.post('/chats/<chat_uuid>/<invite>')
def join(chat_uuid, invite):
    if Chat.query.filter_by(invite=invite).first() is None:
        return jsonify({'error': 'Invalid invite'})

    if (chat := db.session.get(Chat, chat_uuid)) is None:
        return jsonify({'error': 'Invalid chat uuid'})

    user = db.get_or_404(User, session['user'])
    user.chats.append(chat)
    db.session.add(user)
    db.session.commit()

    return jsonify({})


@app.post('/chats')
def create_chat():
    user = db.get_or_404(User, session['user'])

    chat = Chat()
    chat.users.append(user)
    db.session.add(chat)
    db.session.commit()

    return jsonify({'uuid': chat.uuid, 'invite': chat.invite})


@app.get('/messages/<chat_uuid>')
def get_messages(chat_uuid):
    if (chat := db.session.get(Chat, chat_uuid)) is None:
        return jsonify({'error': 'Invalid chat uuid'})

    user = db.get_or_404(User, session['user'])
    if not user.chat_allowed(chat):
        return jsonify({'error': 'Permission denied'})

    return jsonify(list(map(lambda x: x.text, chat.messages)))


@app.put('/messages/<chat_uuid>')
def send_message(chat_uuid):
    if not (message := request.json.get('message')):
        return jsonify({'error': 'Invalid message'})

    if (chat := db.session.get(Chat, chat_uuid)) is None:
        return jsonify({'error': 'Invalid chat uuid'})

    user = db.get_or_404(User, session['user'])
    if not user.chat_allowed(chat):
        return jsonify({'error': 'Permission denied'})

    chat.messages.append(Message(text=message))
    db.session.add(chat)
    db.session.commit()

    return jsonify({})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        admin_chat = Chat()
        admin_chat.messages.append(Message(text=f'The flag is: {os.getenv("FLAG")}'))
        db.session.add(admin_chat)
        db.session.commit()

        admin_user = User()
        admin_user.chats.append(admin_chat)
        db.session.add(admin_user)
        db.session.commit()

        admin_chat_uuid = admin_chat.uuid

        print(admin_chat.uuid, admin_chat.invite)

app.run('0.0.0.0', int(os.getenv('PORT')))
