import time
from datetime import timedelta
import re
import uuid
import os
from Crypto.Util.number import bytes_to_long, isPrime
from flask import Flask, request, render_template, jsonify, session
from libraries.dh import *
from libraries.database import save_session, get_session, delete_expired_sessions, delete_session



FLAG = os.getenv("FLAG")
assert(FLAG)
FLAG_OFFSET = int(os.getenv("FLAG_OFFSET"))
assert(FLAG_OFFSET)
TIMEOUT = int(os.getenv("TIMEOUT"))
assert(TIMEOUT)
NBITS = int(os.getenv("NBITS"))
assert(NBITS)
SECRET_KEY = os.getenv("SECRET_KEY")
assert(SECRET_KEY)


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=TIMEOUT)

def is_hex(s): 
    match = re.fullmatch(r'^[0-9a-fA-F]+$', s) 
    return bool(match)

#Alice answers
def stage1(user_message):
    if is_hex(user_message):
        p = int(user_message, 16)
        if isPrime(p) and p.bit_length() >= NBITS:
            return True, p    
    return False, -1

def stage2(user_message, p, a): 
    if is_hex(user_message):
        g = int(user_message, 16)
        A = pow(g, a, p)
        return True, A
    return False, -1

def stage3(user_message, p, a):  
    if is_hex(user_message):
        B = int(user_message, 16)
        msg = f"Here's the last part of the flag: {FLAG[FLAG_OFFSET:]}"
        key = gen_shared_key(B, a, p)
        return True, aes_encrypt(key, msg)
    return False, "Try again"

def get_custom_response(user_message):
    user_message = user_message.lower()

    if session['stage'] == 0:
        response = "Hi Bob! The connection was interrupted. Can you send me a new prime number p?"
        session['stage'] += 1

    elif session['stage'] == 1:
        val, p = stage1(user_message)
        if val:
            response = "Now send me the generator g"
            session_info = get_session(session['user_id'])
            save_session(session['user_id'], secret=session_info['secret'], prime=p, ts=session_info['ts'])

            session['stage'] += 1
        else:
            response = "Sorry, you have to send me a big enough prime number in hex notation"
    
    elif session['stage'] == 2:
        val, A = stage2(user_message, get_session(session['user_id'])['prime'],  get_session(session['user_id'])['secret'])
        if val:
            response = f"Here's my public key: {hex(A)[2:]}\n Now send me yours"
            session['stage'] += 1
        else:
            response = "Sorry, you have to send me a generator in hex notation"

    elif session['stage'] == 3:
        val, msg = stage3(user_message, get_session(session['user_id'])['prime'],  get_session(session['user_id'])['secret'])
        if val:
            response = "Great! Now we can resume our conversation.\n"
            response += msg
            session['stage'] += 1
        else:
            response = "Sorry, you have to send me your public key in hex notation"

    else:
        response = 'ERROR: Connection lost! Refresh the page'

    return response

#route functions
@app.route("/")
def home():
    session.clear()
    if 'user_id' not in session:
        user_id = str(uuid.uuid4())
        session['user_id'] = user_id
        session['stage'] = 0
        save_session(user_id, secret=-1, prime=None, ts=time.time())
    return render_template("index.html")

@app.route("/get_alice_bob_chat", methods=["GET"])
def get_alice_bob_chat():
    
    g, p = get_parameters()
    a, A = keygen(g, p)
    b, B = keygen(g, p)
    if 'user_id' in session:
        session_info = get_session(session['user_id'])
        save_session(session['user_id'], secret=a, prime=session_info['prime'], ts=session_info['ts'])
    else:
        return jsonify({"error": "Messaggio non valido"}), 400


    # Predefined conversation between Alice and Bob
    conversation = [
        {"sender": "alice", "text": "Hi Bob! Send me the prime number p to start the conversation"},
        {"sender": "bob", "text": f"{hex(p)[2:]}"},
        {"sender": "alice", "text": "Now send me the generator g"},
        {"sender": "bob", "text": f"{hex(g)[2:]}"},
        {"sender": "alice", "text": f"Here is my public key: {hex(A)[2:]}"},
        {"sender": "bob", "text": f"And here is mine: {hex(B)[2:]}"},
        {"sender": "alice", "text": "Perfect! Now we can talk about important stuff"},
    ]

    msgAlice = f"Here's the flag you were asking me for: {FLAG[:FLAG_OFFSET]}ZZZZZZZZZZZZ... ERROR! CONNECTION LOST"
    key = gen_shared_key(B, a, p)
    enc_msg = aes_encrypt(key, msgAlice)
    conversation.append({"sender": "alice", "text": enc_msg})
    return jsonify(conversation)

@app.route("/get_response", methods=["POST"])
def get_response():
    if 'user_id' not in session:
        print(f"", flush=True)
        return jsonify({
            "response": f"Your session has expired. Please refresh the page."
        }), 400

    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Message not valid"}), 400

    #alice response
    bot_response = get_custom_response(user_message)
    return jsonify({"response": bot_response})


@app.route("/convert_secret", methods=["POST"])
def convert_secret():
    data = request.get_json()
    hex_value = data.get("hex", "").strip()
    
    try:
        value = int(hex_value, 16)
        key = hash(value)
        return jsonify(result=hex(bytes_to_long(key))[2:])
    except ValueError:
        return jsonify(result="Invalid value"), 400

# Periodic cleanup of expired sessions
@app.before_request
def cleanup_expired_sessions():
    delete_expired_sessions(TIMEOUT)

    user_id = session.get('user_id')
    if not user_id or get_session(user_id) is None:
        print(f"Session expired for user {user_id}. Resetting session.")
        session.clear()

        if request.endpoint != "home": 
            return jsonify({
                "response": "Your session has expired. Please refresh the page."
            }), 400



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
