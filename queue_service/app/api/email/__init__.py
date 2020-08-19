import redis
from flask import Blueprint, request, jsonify

from app import app, redis_client

bp = Blueprint('email', __name__, url_prefix='/api')


@bp.before_request
def check_api_header():
    header_api_key = request.headers.get('X-Notify-Api-Key')
    if not header_api_key:
        return jsonify({'error': 'The request header does not have an API access key'}), 403
    if header_api_key not in app.config['ALLOWED_TOKENS']:
        return jsonify({'error': 'Access denied'}), 403


@bp.route('/email', methods=['POST'])
def email():
    i = request.get_json()
    try:
        data = i['type'] + '1#2#3' + i['address'] + '1#2#3' + i['message']
    except KeyError as e:
        print(e)
        return 'KeyError', 404
    try:
        redis_client.publish(app.config['CHANNEL'], str(data))
        return "OK", 200
    except redis.exceptions.ConnectionError as e:
        print(e)
        return 'ConnectionError', 404
    except redis.exceptions.DataError as e:
        print(e)
        return 'DataError', 404
