import json
import urllib3
from pymongo import MongoClient
import random
import datetime

mongodb_host = 'localhost'
mongodb_port = '27017'
client  = MongoClient(mongodb_host + ':' + mongodb_port)
db = client['sarai']
collection = db['wunderground-data']

http = urllib3.PoolManager()


def update_database(date,icons,desc,rainfall,precipChance,tempMax,code,location,dayOfWeek,rainfallDayNight):
	print(code)
	print(date)
	print(icons)	
	collection.update({'code':code}, {'$set': {'rainfall':rainfall,'rainfallDayNight':rainfallDayNight,'date':date,'desc': desc,'icons': icons,'precipChance':precipChance, 'tempMax': tempMax, 'location': location, 'dayOfWeek': dayOfWeek}}, upsert=True)

def get_weather_data(place):
	#tokenid = 'F711872F73B24DB9BAC5D2C35DB9D85A'
	#api = 'https://api.weatherlink.com/v1/NoaaExt.json?user=' + data['DeviceId'] + '&pass=' + data['OwnerPass'] + '&apiToken=' + tokenid
	
	api = 'https://api.weather.com/v3/wx/forecast/daily/5day?geocode=' + place['Coords'] + '&units=m&language=en-US&format=json&apiKey=f4664437a9f14d5ba64437a9f13d5b5a'	
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
	update_database(date,icons,desc,rainfall,precipChance,tempMax,place['Code'],place['Location'],dayOfWeek,rainfallDayNight)
	
	
def main():
	data = [
		{
			"Code": "ICALABAR18",
			"Coords": "14.156233,121.262197",
			"Location": "IPB, UP Los Baños, Laguna"
		},
		{
			"Code": "ICAGAYAN3",
			"Coords": "17.410517,21.813614",
			"Location": "ISU Cabagan, Isabela"
		},
		{
			"Code": "ICAGAYAN2",
			"Coords": "16.725611,121.698503",
			"Location": "ISU Echague, Isabela"
		},
		{
			"Code": "ICENTRAL91",
			"Coords": "15.738165,120.928400",
			"Location": "CLSU Muñoz, Nueva Ecija"
		},
		{
			"Code": "ICALABAR25",
			"Coords": "13.944936,121.369765",
			"Location": "DA-QAES Tiaong, Quezon"
		},
		{
			"Code": "IWESTERN635",
			"Coords": "11.102263,122.414762",
			"Location": "WVSU Lambunao, Iloilo City"
		},
		{
			"Code": "ICENTRAL94",
			"Coords": "10.132925,123.546750",
			"Location": "CTU Barili, Cebu"
		},
		{
			"Code": "IBICOLGU2",
			"Coords": "13.192833,123.595327",
			"Location": "BUCAF Guinobatan, Albay"
		},
		{
			"Code": "IMIMAROP6",
			"Coords": "9.443356,118.560378",
			"Location": "WPU Aborlan, Palawan"
		},
		{
			"Code": "IMIMAROP7",
			"Coords": "13.149028,121.187139",
			"Location": "MinSCAT Alcate, Victoria, Oriental Mindoro"
		},
		{
			"Code": "IMIMAROP8",
			"Coords": "13.130432,120.704186",
			"Location": "PhilRice Sta Cruz, Occidental Mindoro"
		},
		{
			"Code": "IZAMBOAN4",
			"Coords": "6.996182,121.929624",
			"Location": "PCA San Ramon, Zamboanga del Sur"
		},
		{
			"Code": "IDAVAORE19",
			"Coords": "6.691228,125.188743",
			"Location": "SPAMAST Kapoc ,Matanao, Davao del Sur"
		},
		{
			"Code": "IDAVAORE20",
			"Coords": "6.489740,125.545582",
			"Location": "SPAMAST Buhangin Campus, Malita, Davao Occ"
		},
		{
			"Code": "INORTHER117",
			"Coords": "7.855571,125.057929",
			"Location": "CMU Maramag, Bukidnon"
		},
		{
			"Code": "INORTHER86",
			"Coords": "8.610266,124.883303",
			"Location": "USTP Claveria, Misamis Oriental"
		},
		{
			"Code": "IREGIONX6",
			"Coords": "7.110252,124.851728",
			"Location": "USM Kabacan, Cotabato"
		},
		{
			"Code": "IWESTERN596",
			"Coords": "10.404912,122.978921",
			"Location": "UPLB-CA La Carlota, Negros Occidental"
		}
    	]
	
	for d in data:
		get_weather_data(d)

if __name__ == "__main__":
    main()





