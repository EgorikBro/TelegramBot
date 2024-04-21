import requests


def get_voyage_between(**params):
    schedule_api_server = 'https://api.rasp.yandex.net/v3.0/search/'
    response = requests.get(schedule_api_server, params=params)
    return response.json()


def get_voyage_by_station(**params):
    schedule_api_server = 'https://api.rasp.yandex.net/v3.0/schedule/'
    response = requests.get(schedule_api_server, params=params)
    return response.json()


def get_stations(**params):
    schedule_api_server = 'https://api.rasp.yandex.net/v3.0/nearest_stations/'
    response = requests.get(schedule_api_server, params=params)
    return response.json()


def get_city(**params):
    schedule_api_server = 'https://api.rasp.yandex.net/v3.0/nearest_settlement/'
    response = requests.get(schedule_api_server, params=params)
    return response.json()


def get_ll(toponym_name):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_name,
        "format": "json"
    }
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if response:
        return response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    else:
        return None
