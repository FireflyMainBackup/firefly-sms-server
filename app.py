from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

TELNYX_API_KEY = os.environ.get('TELNYX_API_KEY', 'KEY019CF05D2C3B8AB8F7E45A9DF657B249')
SUPABASE_URL = 'https://zlplaabcwduydbmrmown.supabase.co'
SUPABASE_KEY = 'sb_publishable_JqAeQQRyRTxORy855Rv3ag_sdzYD6NR'

@app.route('/send', methods=['POST'])
def send_sms():
    data = request.json
    to = data.get('to')
    text = data.get('text')
    from_number = data.get('from', '+447822017856')
    response = requests.post(
        'https://api.telnyx.com/v2/messages',
        headers={
            'Authorization': 'Bearer ' + TELNYX_API_KEY,
            'Content-Type': 'application/json'
        },
        json={'to': to, 'from': from_number, 'text': text}
    )
    return jsonify(response.json()), response.status_code

@app.route('/receive', methods=['POST'])
def receive_sms():
    data = request.json
    payload = data.get('data', {}).get('payload', {})
    from_num = payload.get('from', {}).get('phone_number')
    to_num = payload.get('to', [{}])[0].get('phone_number')
    text = payload.get('text')
    if from_num and text:
        requests.post(
            SUPABASE_URL + '/rest/v1/sms_messages',
            headers={
                'apikey': SUPABASE_KEY,
                'Authorization': 'Bearer ' + SUPABASE_KEY,
                'Content-Type': 'application/json'
            },
            json={'from': from_num, 'to': to_num, 'text': text, 'direction': 'inbound'}
        )
    return jsonify({'status': 'ok'}), 200

@app.route('/')
def health():
    return 'Firefly Hub SMS Server running', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
