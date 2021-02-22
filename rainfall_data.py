import json
import urllib3
from pymongo import MongoClient
import random
import datetime


mongodb_host = 'localhost'
mongodb_port = '3001' #change port depending on database
client  = MongoClient(mongodb_host + ':' + mongodb_port)
db = client['meteor'] #change according to the db name
collection = db['rainfall-historical']

http = urllib3.PoolManager()


def update_database(rainfall_allday,date,place):
	print(date)
	print(rainfall_allday)
	print()
	collection.update({'code':place['code'], 'location': place['location']}, {'$set': {date:rainfall_allday}}, upsert=True)

def get_weather_data(place):
	print(place['code'])
	api = 'http://202.92.144.43/WL/JSON/' + place['code'] + '.json';
	print(api)

	rainfall_data = http.request('GET', api)
	rainfall_dict = json.loads(rainfall_data.data.decode('UTF-8'))
	rainfall_allday = (float(rainfall_dict['davis_current_observation']['rain_day_in']) * 25.4)
	t = datetime.date.today().strftime('%m-%d-%Y')
	update_database(rainfall_allday, t, place)

	
def main():
	data = [
		{
			"code": "BUCAF-Albay",
			"location": "BUCAF Guinobatan, Albay"
		},
		{
			"code": "CLSU-Munoz",
			"location": "CLSU Muñoz, Nueva Ecija"
		},
		{
			"code": "CMU-Maramag",
			"location": "CMU Maramag, Bukidnon"
		},
		{
			"code": "CTU-Barili",
			"location": "CTU Barili, Cebu"
		},
		{
			"code": "DAQAES-Tiaong",
			"location": "DA-QAES Tiaong, Quezon"
		},
		{
			"code": "IPB-UPLB",
			"location": "IPB, UP Los Baños, Laguna"
		},
		{
			"code": "ISU-Cabagan",
			"location": "ISU Cabagan, Isabela"
		},
		{
			"code": "ISU-Echague",
			"location": "ISU Echague, Isabela"
		},
		{
			"code": "MINSCAT-Mindoro",
			"location": "MinSCAT Alcate, Victoria, Oriental Mindoro"
		},
		{
			"code": "MMSU-Batac",
			"location": "MMSU Batac Ilocos Norte"
		},
		{
			"code": "PCA-Zamboanga",
			"location": "PCA San Ramon, Zamboanga del Sur"
		},
		{
			"code": "PHILRICE-Mindoro",
			"location": "PhilRice Sta Cruz, Occidental Mindoro"
		},
		{
			"code": "SPAMAST-Malita",
			"location": "SPAMAST Buhangin Campus, Malita, Davao Occidental"
		},
		{
			"code": "SPAMAST-Matanao",
			"location": "SPAMAST Kapoc ,Matanao, Davao del Sur"
		},
		{
			"code": "UPLBCA-LaGranja",
			"location": "UPLB-CA La Carlota, Negros Occidental"
		},
		{
			"code": "USM-Kabacan",
			"location": "USM Kabacan, Cotabato"
		},
		{
			"code": "USTP-Claveria",
			"location": "USTP Claveria, Misamis Oriental"
		},
		{
			"code": "WPU-Aborlan",
			"location": "WPU Aborlan, Palawan"
		},
		{
			"code": "WVSU-Iloilo",
			"location": "WVSU Lambunao, Iloilo City"
		},
    	]
	
	for d in data:
		get_weather_data(d)

if __name__ == "__main__":
    main()





