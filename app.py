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
    
    to = data.get('to', '').replace(' ', '')
    from_num = data.get('from', '').replace(' ', '')
    text = data.get('text', '')
    
    if not to.startswith('+'):
        to = '+' + to
    if not from_num.startswith('+'):
        from_num = '+' + from_num
    
    resp = requests.post(
        'https://api.telnyx.com/v2/messages',
        headers={
            'Authorization': 'Bearer ' + key,
            'Content-Type': 'application/json'
        },
        json={'to': to, 'from': from_num, 'text': text}
    )
    
    print('Telnyx response: ' + str(resp.status_code) + ' - ' + resp.text)
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
