import json
import urllib3
from pymongo import MongoClient
import random
import datetime

mongodb_host = 'localhost'
mongodb_port = '3001' #change port depending on database
client  = MongoClient(mongodb_host + ':' + mongodb_port)
db = client['meteor'] #change according to the db name
collection = db['wunderground-data']

http = urllib3.PoolManager()


def update_database(date,icons,desc,rainfall,precipChance,tempMax,place,dayOfWeek,rainfallDayNight):
	print("Updating:",place['code'])
	print(date)
	print(rainfall)
	print(tempMax)
	print()	
	collection.update({'code':place['code'], 'location': place['location']}, {'$set': {'rainfall':rainfall,'rainfallDayNight':rainfallDayNight,'date':date,'desc': desc,'icons': icons,'precipChance':precipChance, 'tempMax': tempMax, 'dayOfWeek': dayOfWeek}}, upsert=True)

def get_weather_data(place):
	api = 'https://api.weather.com/v3/wx/forecast/daily/5day?geocode=' + place['coords'] + '&units=m&language=en-US&format=json&apiKey=f4664437a9f14d5ba64437a9f13d5b5a'	
	wunderground_data = http.request('GET', api)	
	wunderground_dict = json.loads(wunderground_data.data.decode('UTF-8'))
	date = []
	for i in range(6):
		t = datetime.date.today() + datetime.timedelta(days=i)
		date.append(t.strftime('%m/%d'))
	icons = wunderground_dict['daypart'][0]['iconCode']
	desc = wunderground_dict['daypart'][0]['wxPhraseLong']
	rainfall = wunderground_dict['qpf']
	rainfallDayNight = wunderground_dict['daypart'][0]['qpf']
	dayOfWeek = wunderground_dict['dayOfWeek']
	precipChance = wunderground_dict['daypart'][0]['precipChance']
	tempMax = wunderground_dict['daypart'][0]['temperature']
	update_database(date,icons,desc,rainfall,precipChance,tempMax,place,dayOfWeek,rainfallDayNight)
	
	
def main():
	data = [
		{
			"code": "IPB-UPLB",
			"coords": "14.156233,121.262197",
			"location": "IPB, UP Los Baños, Laguna"
		},
		{
			"code": "MMSU-Batac",
			"coords": "18.054028,120.545667",
			"location": "MMSU Batac Ilocos Norte"
		},
		{
			"code": "ISU-Cabagan",
			"coords": "17.410517,21.813614",
			"location": "ISU Cabagan, Isabela"
		},
		{
			"code": "ISU-Echague",
			"coords": "16.725611,121.698503",
			"location": "ISU Echague, Isabela"
		},
		{
			"code": "CLSU-Munoz",
			"coords": "15.738165,120.928400",
			"location": "CLSU Muñoz, Nueva Ecija"
		},
		{
			"code": "DAQAES-Tiaong",
			"coords": "13.944936,121.369765",
			"location": "DA-QAES Tiaong, Quezon"
		},
		{
			"code": "WVSU-Iloilo",
			"coords": "11.102263,122.414762",
			"location": "WVSU Lambunao, Iloilo City"
		},
		{
			"code": "CTU-Barili",
			"coords": "10.132925,123.546750",
			"location": "CTU Barili, Cebu"
		},
		{
			"code": "BUCAF-Albay",
			"coords": "13.192833,123.595327",
			"location": "BUCAF Guinobatan, Albay"
		},
		{
			"code": "WPU-Aborlan",
			"coords": "9.443356,118.560378",
			"location": "WPU Aborlan, Palawan"
		},
		{
			"code": "MINSCAT-Mindoro",
			"coords": "13.149028,121.187139",
			"location": "MinSCAT Alcate, Victoria, Oriental Mindoro"
		},
		{
			"code": "PHILRICE-Mindoro",
			"coords": "13.130432,120.704186",
			"location": "PhilRice Sta Cruz, Occidental Mindoro"
		},
		{
			"code": "PCA-Zamboanga",
			"coords": "6.996182,121.929624",
			"location": "PCA San Ramon, Zamboanga del Sur"
		},
		{
			"code": "SPAMAST-Matanao",
			"coords": "6.691228,125.188743",
			"location": "SPAMAST Kapoc ,Matanao, Davao del Sur"
		},
		{
			"code": "SPAMAST-Malita",
			"coords": "6.489740,125.545582",
			"location": "SPAMAST Buhangin Campus, Malita, Davao Occidental"
		},
		{
			"code": "CMU-Maramag",
			"coords": "7.855571,125.057929",
			"location": "CMU Maramag, Bukidnon"
		},
		{
			"code": "USTP-Claveria",
			"coords": "8.610266,124.883303",
			"location": "USTP Claveria, Misamis Oriental"
		},
		{
			"code": "USM-Kabacan",
			"coords": "7.110252,124.851728",
			"location": "USM Kabacan, Cotabato"
		},
		{
			"code": "UPLBCA-LaGranja",
			"coords": "10.404912,122.978921",
			"location": "UPLB-CA La Carlota, Negros Occidental"
		}
    	]
	
	for d in data:
		get_weather_data(d)

if __name__ == "__main__":
    main()





