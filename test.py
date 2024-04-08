import requests
import json

with open('api.json', encoding='utf-8') as json_file:
    n = 0
    for i in json_file:
        for j in i[2]:
            n += 1
            print(i)
            print(n)
