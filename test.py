import requests
import json

from data import db_session
from data.cities import Cities
from data.stations import Stations

db_session.global_init("db/codes.db")
db_sess = db_session.create_session()
with open('api.json', encoding='utf-8') as json_file:
    n = 0
    f = json.load(json_file)
    for i in f['countries']:
        for j in i['regions']:
            for k in j['settlements']:
                print('===')
                if k["codes"].get("yandex_code"):
                    print(f'{k["title"]} - {k["codes"]["yandex_code"]}!')
                    print('---')
                    cities = Cities(city=k['title'], yandex_code=k["codes"]["yandex_code"])
                    db_sess.add(cities)

                for p in k['stations']:
                    print(f'{p["title"]} - {p["codes"]["yandex_code"]}')
                    stations = Stations(station=p["title"], city=k['title'], yandex_code=p["codes"]["yandex_code"])
                    db_sess.add(stations)
    db_sess.commit()
