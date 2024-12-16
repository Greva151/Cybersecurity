from flask import Flask, request, render_template, g, send_file, redirect, url_for, session, jsonify
from random import randbytes
import os
import db, utils

app = Flask(__name__)
app.config['SECRET_KEY'] = hex(int.from_bytes(randbytes(256)))

CODE = utils.get_random_code()
ACCESS_LOG_PAGE = utils.get_random_url()
FLAG = os.getenv('FLAG')

@app.route('/')
def index():
    message = session.pop('index_message', None)
    return render_template('index.html', message=message, title="Home", access_log_page=ACCESS_LOG_PAGE)


@app.route('/'+ACCESS_LOG_PAGE)
def access_log():

    accesses = [
        {"id": 1, "timestamp": "2024-12-14 10:00"},
        {"id": 2, "timestamp": "2024-12-14 12:00"}
    ]

    message = session.pop('login_message', None)
    
    return render_template('access_log.html', accesses=accesses, message=message, title="Access Log")


@app.route('/login', methods=['POST'])
def login():
    
    if not request.form:
        session['login_message'] = 'Missing data!'
        return redirect(url_for('access_log'))

    if 'username' not in request.form or 'password' not in request.form:
        session['login_message'] = 'Missing data!'
        return redirect(url_for('access_log'))

    username = request.form['username']
    password = request.form['password']

    if username != 'admin':
        session['login_message'] = 'Only admin can access the access log!'

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

    if not utils.check_query(query):
        session['login_message'] = 'Invalid query!'
        return redirect(url_for('access_log'))

    user = db.query_db(query, one=True)

    if user:
        n, e, ciphertext = utils.generate_rsa(CODE)
        file = utils.create_pcap(n, e, ciphertext)

        return send_file(file, mimetype="application/vnd.tcpdump.pcap", as_attachment=True, download_name="access_log.pcap")
    else:
        session['login_message'] = 'Login failed!'
        return redirect(url_for('access_log'))
    

@app.route("/unlock", methods=["POST"])
def unlock():

    if request.method != 'POST':
        return redirect(url_for('index'))

    if not request.form:
        session['index_message'] = 'Missing data!'
        return redirect(url_for('index'))
    
    digit1 = request.form.get('digit1')
    digit2 = request.form.get('digit2')
    digit3 = request.form.get('digit3')
    digit4 = request.form.get('digit4')
    digit5 = request.form.get('digit5')
    digit6 = request.form.get('digit6')
    digit7 = request.form.get('digit7')
    digit8 = request.form.get('digit8')

    if not digit1 or not digit2 or not digit3 or not digit4 or not digit5 or not digit6 or not digit7 or not digit8:
        session['index_message'] = 'Missing data!'
        return redirect(url_for('index'))
    
    code = digit1 + digit2 + digit3 + digit4 + digit5 + digit6 + digit7 + digit8

    if code == CODE:
        return render_template('unlocked.html', flag=FLAG, title="Unlocked!")
    else:
        session['index_message'] = 'Invalid code!'
        return redirect(url_for('index'))
    
@app.errorhandler(404)
def not_found(error):
  return render_template('400.html', code=404, error=error, title=str(404)), 404

@app.errorhandler(403)
def forbidden(error):
  return render_template('400.html', code=403, error=error, title=str(403)), 403

@app.errorhandler(401)
def unauthorized(error):
  return render_template('400.html', code=401, error=error, title=str(401)), 401

@app.errorhandler(405)
def not_allowed(error):
  return render_template('400.html', code=405, error=error, title=str(405)), 405

@app.errorhandler(500)
def not_allowed(error):
  return render_template('400.html', code=500, error=error, title=str(500)), 500