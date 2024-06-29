import json
import os
import requests

from Previsao import Previsao

def criaPrevisao(cidade: str, estado: str, ):
	print(cidade, estado)
	API_KEY = "PREENCHER"
	r = requests.get(f"http://api.weatherbit.io/v2.0/forecast/daily?key={API_KEY}&lang=pt&days=7&city={cidade}&state={estado}")
	
	if r.status_code != 200:
		return 
	response = r.json()
	
	previsao = {}

	for i in range(7):
		previsao[response["data"][i]["datetime"]] = Previsao(response['city_name'], response["country_code"],
			response["data"][i]["app_min_temp"], response["data"][i]["app_max_temp"],
			response["data"][i]["weather"]["description"])

	salvaPrevisao(cidade, estado, response)

	return previsao

def salvaPrevisao(cidade, estado, dados):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	temp_dir = dir_path + "/../temp"
	with open(f"{temp_dir}/{'-'.join(estado.split())}-{cidade}.json", "w", encoding="utf-8") as f:
		json.dump(dados, f, ensure_ascii=False, indent=4)

def criaTemp():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	temp_dir = dir_path + "/../temp"
	if not os.path.exists(temp_dir):
   		os.makedirs(temp_dir)


