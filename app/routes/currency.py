# app/routes/currency.py

from flask import Blueprint, request, jsonify
from flask import jsonify
from dotenv import load_dotenv
import requests
import os
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()
bp = Blueprint('currency', __name__, url_prefix='/currency')

@bp.route('/check', methods=['GET'])
def check_currency():
    try:
        base = 'https://v6.exchangerate-api.com'
        api_key = os.getenv('EXCHANGE_RATE_API_KEY')
        threshold = request.args.get('threshold', type=float)
        baseCurrency = request.args.get('baseCurrency', default='USD', type=str)
        api_url = f'{base}/v6/{api_key}/latest/{baseCurrency}'

        response = requests.get(api_url)

        if response.status_code == 200:
            conversion_rates = response.json().get("conversion_rates")
            result = {currency: rate for currency, rate in conversion_rates.items() if rate > threshold}
            return jsonify(result)

        else:
            # Log error details for debugging
            logging.error(f'Failed to fetch data from API: {response.text}')
            return jsonify({"error": "Failed to fetch data from API"}), 500

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        return jsonify({"error": "An error occurred"}), 500