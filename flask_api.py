from flask import Flask, jsonify, request
from loguru import logger

app = Flask(__name__)


@app.route('/notify', methods=['POST'])
def notify():
    post_data = request.get_json()
    event = post_data.get('event')
    data = post_data.get('data')
    logger.debug(f'received event {event}, data {data}')
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
