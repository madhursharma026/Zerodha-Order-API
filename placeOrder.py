import requests
import pandas as pd
from flask_cors import CORS
from kiteconnect import KiteConnect
from flask import Flask, request, jsonify
app = Flask(__name__)
CORS(app)
kite = KiteConnect(api_key="qcco08jfkec80s8j")

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8'
}

def place_order(symbol, quantity, request_token):
    try:
        data = kite.generate_session(str(request_token), api_secret="cu1jpl4q5spflx3tppfxmsjgaylqkm1m")
        kite.set_access_token(data["access_token"])
        order_id = kite.place_order(
            tradingsymbol=symbol,
            exchange=kite.EXCHANGE_NSE,
            transaction_type=kite.TRANSACTION_TYPE_BUY,
            quantity=quantity,
            variety=kite.VARIETY_AMO,
            order_type=kite.ORDER_TYPE_MARKET,
            product=kite.PRODUCT_CNC,
            validity=kite.VALIDITY_DAY
        )
        return order_id
    except Exception as e:
        return str(e)

def sell_order(symbol, quantity, request_token):
    try:
        data = kite.generate_session(str(request_token), api_secret="cu1jpl4q5spflx3tppfxmsjgaylqkm1m")
        kite.set_access_token(data["access_token"])
        order_id = kite.place_order(
            tradingsymbol=symbol,
            exchange=kite.EXCHANGE_NSE,
            transaction_type=kite.TRANSACTION_TYPE_SELL,
            quantity=quantity,
            variety=kite.VARIETY_AMO,
            order_type=kite.ORDER_TYPE_MARKET,
            product=kite.PRODUCT_CNC,
            validity=kite.VALIDITY_DAY
        )
        return order_id
    except Exception as e:
        return str(e)

# serverURL/
@app.route('/', methods=['GET'])
def home_route():
    return "Hello, This is home route"

# serverURL/getRequestToken
@app.route('/getRequestToken', methods=['GET'])
def getRequestToken_route():
    return f'<a href="https://kite.zerodha.com/connect/login?v=3&api_key=qcco08jfkec80s8j">Click here to go to Kite Zerodha</a>'

# serverURL/place_order?symbol=INFY&quantity=1&request_token=your_request_token
@app.route('/place_order', methods=['GET'])
def place_order_route():
    symbol = request.args.get('symbol')
    quantity = int(request.args.get('quantity'))
    request_token = request.args.get('request_token')
    order_id = place_order(symbol, quantity, request_token)
    return jsonify({"order_id": order_id})

# serverURL/place_order
@app.route('/place_order', methods=['POST'])
def place_order_route_post():
    symbol = request.json.get('symbol')
    quantity = int(request.json.get('quantity'))
    request_token = request.json.get('request_token')
    order_id = place_order(symbol, quantity, request_token)
    return jsonify({"order_id": order_id})

# serverURL/sell_order?symbol=INFY&quantity=1&request_token=your_request_token
@app.route('/sell_order', methods=['GET'])
def sell_order_route():
    symbol = request.args.get('symbol')
    quantity = int(request.args.get('quantity'))
    request_token = request.args.get('request_token')
    order_id = sell_order(symbol, quantity, request_token)
    return jsonify({"order_id": order_id})

# serverURL/sell_order
@app.route('/sell_order', methods=['POST'])
def sell_order_route_post():
    symbol = request.json.get('symbol')
    quantity = int(request.json.get('quantity'))
    request_token = request.json.get('request_token')
    order_id = sell_order(symbol, quantity, request_token)
    return jsonify({"order_id": order_id})

def fetch_option_chain(option_type):
    baseurl = "https://www.nseindia.com/"
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol="+option_type
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                             'like Gecko) '
                             'Chrome/80.0.3987.149 Safari/537.36',
               'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
    session = requests.Session()
    request = session.get(baseurl, headers=headers, timeout=5)
    cookies = dict(request.cookies)
    response = session.get(url, headers=headers, timeout=5, cookies=cookies)
    return (response.json())

# serverURL/option_chain
@app.route('/option_chain', methods=['GET'])
def option_chain():
    try:
        option_type = request.args.get('option_type')
        option_chain = fetch_option_chain(option_type)
        return jsonify(option_chain)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
