import requests


def get_voyage(**params):
    schedule_api_server = 'https://api.rasp.yandex.net/v3.0/search/'
    response = requests.get(schedule_api_server, params=params)
    return response.json()