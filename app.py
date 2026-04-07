from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

TELNYX_API_KEY = os.environ.get('TELNYX_API_KEY', 'KEY019CF05D2C3B8AB8F7E45A9DF657B249')
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://zlplaabcwduydbmrmown.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'sb_publishable_JqAeQQRyRTxORy855Rv3ag_sdzYD6NR')

def log_to_supabase(from_num, to_num, text, direction):
    try:
        requests.post(
            f'{SUPABASE_URL}/rest/v1/sms_messages',
            headers={
                'apikey': SUPABASE_KEY,
                'Authorization': f'Bearer {SUPABASE_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'from': from_num,
                'to': to_num,
                'text': text,
                'direction': direction
            }
        )
    except Exception as e:
        print(f'Supabase log error: {e}')

@app.route('/send', methods=['POST'])
def send_sms():
    data = request.json
    to = data.get('to')
    text = data.get('text')
    from_number = data.get('from', '+447822017856')

    if not to or not text:
        return jsonify({'error': 'Missing to or text'}), 400

    response = requests.post(
        'https://api.telnyx.com/v2/messages',
        headers={
            'Authorization': f'Bearer {TELNYX_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={'to': to, 'from': from_number, 'text': text}
    )

    if response.status_code == 200:
        log_to_supabase(from_number, to, text, 'outbound')

    return jsonify(response.json()), response.status_code

@app.route('/receive', methods=['POST'])
def
