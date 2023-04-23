from flask import Flask, jsonify
from flask_cors import CORS
from scraping.bloomberg_com import bloomberg_com
from scraping.investing_com import get_pair
from api.oanda_api import OandaApi

app = Flask(__name__)
CORS(app)

@app.route('/api/test')
def test():
    return jsonify(dict(message='hello world'))

@app.route('/api/headlines')
def headlines():
    return jsonify(bloomberg_com())

@app.route('/api/technicals/<pair>/<tfs>')
def technicals(pair, tfs):
    data = get_pair(pair, tfs)
    if data is None:
        return jsonify(dict(message='No data found'))
    else:
        return jsonify(data)
    
@app.route('/api/prices/<pair>/<granularity>/<count>')
def prices(pair, granularity, count):
    data = OandaApi().web_api_candles(pair, granularity, count)
    if data is None:
        return jsonify(dict(message='No data found'))
    else:
        return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)