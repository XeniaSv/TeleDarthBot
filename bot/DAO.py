import json

file_name_currencies = 'currencies.json'
with open(file_name_currencies) as fl:
    currencies = json.load(fl)

file_name_cities = 'cities.json'
with open(file_name_cities) as fr:
    cities = json.load(fr)
