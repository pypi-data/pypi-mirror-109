import requests
from firstimpression.api.bbc import *
from firstimpression.api.ns import *
from firstimpression.api.nu_nl import *
from firstimpression.api.traffic import *



def request(url, header=None, params=None):
    if header is None and params is None:
        return requests.get(url)
    elif header is None:
        return requests.get(url, params=params)
    elif params is None:
        return requests.get(url, headers=header)
    else:
        return requests.get(url, headers=header, params=params)


def request_json(url, header=None, params=None):
    response = request(url, header, params)
    return response.json()
