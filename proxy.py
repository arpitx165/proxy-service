import requests


def get(url, headers=None, params={}, timeout=5, data={}):
    return requests.get(url, headers=headers, params=params, timeout=(timeout, timeout))


def post(url, headers=None, params={}, timeout=5, data={}):
    return requests.post(url, headers=headers, params=params, data=data, timeout=(timeout, timeout))


def patch(url, headers=None, params={}, timeout=5, data={}):
    return requests.patch(url, headers=headers, params=params, data=data, timeout=(timeout, timeout))


def put(url, headers=None, params={}, timeout=5, data={}):
    return requests.put(url, headers=headers, params=params, data=data, timeout=(timeout, timeout))


def delete(url, headers=None, params={}, timeout=5, data={}):
    return requests.delete(url, headers=headers, params=params, data=data, timeout=(timeout, timeout))
