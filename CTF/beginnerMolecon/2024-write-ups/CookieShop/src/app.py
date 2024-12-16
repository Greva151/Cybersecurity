from flask import Flask, request, render_template, redirect, url_for, session, make_response
import os
import base64
import json

FLAG = os.getenv('FLAG')

products = [
    {
        'name': 'ptmSticker',
        'price': 1,
        'description': 'A very nice sticker to decorate your belongings. Show off your support with this stylish sticker!',
        'image_path': 'images/1.png'
    },
    {
        'name': 'm0lecon 2022 vip pass',
        'price': 100,
        'description': 'An exclusive VIP pass for m0lecon 2025. Gain access to all areas and enjoy special privileges at the event.',
        'image_path': 'images/2.png'
    },
    {
        'name': 'flag',
        'price': 1000,
        'description': 'The ultimate prize. Obtain the flag and prove your prowess. This is the most coveted item in the shop.',
        'image_path': 'images/3.png'
    },
]

app = Flask(__name__)

app.secret_key = 'super_secret_key'

@app.route('/')
def index():

    if 'nothing' not in request.cookies:
        balance = 10
        response = make_response(render_template('index.html', products=products, balance=balance))
        response.set_cookie('nothing', base64.b64encode(json.dumps({'balance': balance}).encode()).decode())
        return response
    else:
        balance = json.loads(base64.b64decode(request.cookies.get('nothing')))['balance']
    
    return render_template('index.html', products=products, balance=balance)

@app.route('/buy', methods=['POST'])
def buy():
    balance = json.loads(base64.b64decode(request.cookies.get('nothing')))['balance']

    product_name = request.form['product_name']
    product = next((p for p in products if p['name'] == product_name), None)

    print(product, balance)
    if product is None:
        message = 'Product not found'
        return redirect(url_for('index'))
    
    if balance < product['price']:
        message = 'Not enough balance'
        return redirect(url_for('index'))
    
    balance -= product['price']

    if product['name'] == 'flag':
        message = FLAG
    else:
        message = 'Product bought, it will be shipped soon'


    response = make_response(render_template('index.html', products=products, balance=balance, message=message))
    response.set_cookie('nothing', base64.b64encode(json.dumps({'balance': balance}).encode()).decode())

    return response