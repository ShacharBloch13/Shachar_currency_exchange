# app/routes/currency.py

from flask import Blueprint, request, jsonify, Flask
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()
bp = Blueprint('currency', __name__, url_prefix='/currency')

app = Flask(__name__)
CORS(app)

@bp.route('/check', methods=['GET'])
def check_currency():
    try:
        base = 'https://v6.exchangerate-api.com'
        api_key = os.getenv('EXCHANGE_RATE_API_KEY')
        sum = request.args.get('sum', default=1, type=float)
        baseCurrency = request.args.get('baseCurrency', default='USD', type=str)
        api_url = f'{base}/v6/{api_key}/latest/{baseCurrency}'

        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            conversion_rates = data.get("conversion_rates")
            converted_values = {currency: rate * sum for currency, rate in conversion_rates.items()}
            sorted_converted_values = dict(sorted(converted_values.items(), key=lambda item: item[1], reverse=True))
            
            # if we just want for api platform (like postman)
            return jsonify(converted_values)

            #if we want to arrange in a table for HTML
            # table = "<table><tr><th>Currency</th><th>Value</th></tr>"
            # for currency, value in sorted_converted_values.items():
            #     table += f"<tr><td>{currency}</td><td>{value}</td></tr>"
            # table += "</table>"
            # return table

        else:
            # Log error details for debugging
            logging.error(f'Failed to fetch data from API: {response.text}')
            return jsonify({"error": "Failed to fetch data from API"}), 500

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        return jsonify({"error": "An error occurred"}), 500