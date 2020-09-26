from flask import Flask, jsonify, request
from redis import Redis
from urllib.parse import urlparse
from middleware import RedisMiddleWare
from proxy import get, put, patch, post, delete
import json

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
RedisMiddleWare.set_redis(redis)

request_method_mapping = {
    'get': get,
    'post': post,
    'patch': patch,
    'delete': delete,
    'put': put
}


def url_validators(url):
    res = urlparse(url)
    status = all([res.scheme, res.netloc])
    if not status or (status and res.scheme and res.scheme.lower() != 'https'):
        return 'Invalid url'


def request_method_validators(request_method):
    if not request_method.lower() in ['get', 'put', 'post', 'patch', 'delete']:
        return 'invalid request type'


def request_validators(request_body):
    message = url_validators(request_body.get('url'))
    if message:
        return message
    message = request_method_validators(request_body.get('httpRequestType'))
    if message:
        return message


def get_message(exception_ref):
    if hasattr(exception_ref, 'message'):
        return exception_ref.message
    return str(exception_ref)


@app.before_request
def rate_limiting():
    request_body = request.get_json()
    if request_body:
        st = RedisMiddleWare.check_limit(request_body)
        if st:
            return jsonify({'requestBlocked': True}), 429


@app.route('/triggerRequest', methods=['POST'])
def trigger_request():
    try:
        request_body = request.get_json()
        message = request_validators(request_body)
        if message:
            return jsonify({'status': 'fail', 'error': message}), 422
        url = request_body.get('url')
        headers = request_body.get('headers')
        params = request_body.get('params')
        http_method = request_body.get('httpRequestType')
        body = request_body.get('requestBody') if request_body.get('requestBody') else {}
        is_stringify = request_body.get('requestBodyStringify')
        if is_stringify:
            body = json.dumps(body)
        res = request_method_mapping[http_method.lower()](url, headers=headers, params=params, data=body)
        data = None
        if hasattr(res, 'data'):
            data = res.data
        elif hasattr(res, 'text'):
            data = res.text
        return jsonify({'status': 'success', 'data': {'reqStatus': res.status_code, 'reqData': data, 'url': url}}), 200
    except Exception as e:
        return jsonify({'status': 'Fail', 'error': get_message(e)}), 500


@app.route('/health')
def health():
    try:
        res = redis.ping()
        return jsonify({'status': 'Ready', 'health_check': [{'redis': res}]}), 200
    except Exception as e:
        return jsonify({'status': 'Live', 'health_check': [{'redis': False}], 'error': get_message(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
