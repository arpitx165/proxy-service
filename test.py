import requests


def test_int():
    url = 'http://127.0.0.1:5000/triggerRequest'
    body = {
        "clientId": "test0001",
        "url": "https://jsonplaceholder.typicode.com/posts",
        "params": {"userId": 1},
        "headers": {"Content-type": "application/json; charset=UTF-8"},
        "httpRequestType": "GET",
        "requestBody": {},
    }
    res = requests.post(url, json=body)
    assert res.status_code == 200
    assert res.json()['data']['reqData'] != None

test_int()