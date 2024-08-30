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
	collection.update_one({'code':place['code'], 'location': place['location'], 'coordinates':place['coords']}, {'$set': {'rainfall':rainfall,'rainfallDayNight':rainfallDayNight,'date':date,'desc': desc,'icons': icons,'precipChance':precipChance, 'tempMax': tempMax, 'dayOfWeek': dayOfWeek}}, upsert=True)

def get_weather_data(place):
	api = 'https://api.weather.com/v3/wx/forecast/daily/5day?geocode=' + place['coords'] + '&units=m&language=en-US&format=json&apiKey=8de49c14cda548f7a49c14cda568f7b1'	
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
			"coords": "17.410517,121.813614",
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
		},
		{
			"code": "BENGUET,TUBLAY_AWS_SITE01",
			"coords": "16.47686,120.65982",
			"location": "Benguet, Tublay AWS"
		},
		{
			"code": "BENGUET,BUNGUIAS_AWS_SITE02",
			"coords": "16.69085,120.77909",
			"location": "Benguet, Bunguias AWS"
		},
		{
			"code": "BENGUET,ITOGON,ISRI_AWS_SITE03",
			"coords": "16.34874,120.67166",
			"location": "Benguet, Itogon, ISRI AWS"
		},
		{
			"code": "LAGUNA,SINOLOAN, LANDGRANT_AWS_SITE04",
			"coords": "14.49039,121.51458",
			"location": "Laguna, Sinologan, Landgrant AWS"
		},
		{
			"code": "BATANGAS, LOBO AWS",
			"coords": "13.67721,121.25239",
			"location": "Batangas, Lobo AWS"
		},
		{
			"code": "LIGTAS BOKOD AWS",
			"coords": "16.55000,120.84000",
			"location": "Ligtas Bokod AWS"
		},
		{
			"code": "LIGTAS MANKAYAN AWS",
			"coords": "16.82303,120.81789",
			"location": "Ligtas Mankayan AWS"
		},
		{
			"code": "LIGTAS ITOGON AWS",
			"coords": "16.40175,120.64647",
			"location": "Ligtas Itogon AWS"
		},
		{
			"code": "LIGTAS UEP SAMAR AWS",
			"coords": "12.50878,124.66461",
			"location": "Ligtas UEP Samar AWS"
		},
		{
			"code": "REGION 4A DA BRGY. CALAWIS",
			"coords": "14.65002,121.24125",
			"location": "Region 4A DA Brgy. Calawis"
		},
		{
			"code": "Region 4A DA AMADEO CAVITE",
			"coords": "14.1717271,120.9342409",
			"location": "Region 4A DA Amadeo Cavite"
		},
		{
			"code": "Region 4A DA ATIMONAN QUEZON",
			"coords": "13.9911032,121.8987722",
			"location": "Region 4A DA Atimonan Quezon"
		},
		{
			"code": "Region 4A DA BUENAVISTA QUEZON",
			"coords": "13.72249,122.42407",
			"location": "Region 4A DA Buenavista Quezon"
		},
		{
			"code": "Region 4A DA CAVINTI LAGUNA",
			"coords": "14.2664331,121.5471692",
			"location": "Region 4A DA Cavinti Laguna"
		},
		{
			"code": "Region 4A DA GEN. NAKAR QUEZON",
			"coords": "14.7715568,121.6370445",
			"location": "Region 4A DA Gen. Nakar Quezon"
		},
		{
			"code": "Region 4A DA LARES Batangas",
			"coords": "13.96009,121.16844",
			"location": "Region 4A DA Lares Batangas"
		},
		{
			"code": "Region 4A DA MARAGONDON CAVITE",
			"coords": "14.24767,120.79567",
			"location": "Region 4A DA Maragondon Cavite"
		},
		{
			"code": "Region 4A DA MORONG RIZAL",
			"coords": "14.5120217,121.238134",
			"location": "Region 4A DA Morong Rizal"
		},
		{
			"code": "Region 4A DA PILA LAGUNA",
			"coords": "14.2215023,121.3703309",
			"location": "Region 4A DA Pila Laguna"
		},
		{
			"code": "Region 4A DA RARES TANAY RIZAL",
			"coords": "14.57667,121.33936",
			"location": "Region 4A DA Rares Tanay Rizal"
		},
		{
			"code": "Region 4A DA SAN LUIS BATANGAS",
			"coords": "13.8324203,120.9442319",
			"location": "Region 4A DA San Luis Batangas"
		},
		{
			"code": "Region 4A DA SARIAYA QUEZON",
			"coords": "14.001996297761314,121.52269698679446",
			"location": "Region 4A DA Sariaya Quezon"
		},
    ]
	
	for d in data:
		get_weather_data(d)

if __name__ == "__main__":
    main()





