import requests
import json

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
                for p in k['stations']:
                    print(f'{p["title"]} - {p["codes"]["yandex_code"]}')
