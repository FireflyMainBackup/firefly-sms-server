from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def health():
    return 'OK'

@app.route('/send', methods=['POST', 'OPTIONS'])
def send_sms():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    key = os.environ.get('TELNYX_API_KEY', '')
    resp = requests.post(
        'https://api.telnyx.com/v2/messages',
        headers={
            'Authorization': 'Bearer ' + key,
            'Content-Type': 'application/json'
        },
        json={
            'to': data.get('to'),
            'from': data.get('from'),
            'text': data.get('text')
        }
    )
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
