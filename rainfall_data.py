import json
import urllib3
from pymongo import MongoClient
import random
import datetime


mongodb_host = 'localhost'
mongodb_port = '27017'
client  = MongoClient(mongodb_host + ':' + mongodb_port)
db = client['sarai']
collection = db['rainfall-historical']

http = urllib3.PoolManager()


def update_database(rainfall_allday,date,code):
	print(date)
	print(rainfall_allday)
	print(code)
	#print(len(rainfall_30))
	#if(len(rainfall_30)==30):
	#	rainfall_30.pop()
	
	#rainfall_30.insert(0,data)
	#print(rainfall_30)
	collection.update({'code':code}, {'$set': {date:rainfall_allday}}, upsert=True)

def get_weather_data():
	#tokenid = 'F711872F73B24DB9BAC5D2C35DB9D85A'
	#api = 'https://api.weatherlink.com/v1/NoaaExt.json?user=' + data['DeviceId'] + '&pass=' + data['OwnerPass'] + '&apiToken=' + tokenid
	print(collection.find({},{'code':1}))
	for x in collection.find({},{'code':1}):
		print(x['code'])
		api = 'http://202.92.144.43/WL/JSON/' + x['code'] + '.json';
		print(api)

		rainfall_data = http.request('GET', api)
		rainfall_dict = json.loads(rainfall_data.data.decode('UTF-8'))
		rainfall_allday = (float(rainfall_dict['davis_current_observation']['rain_day_in']) * 25.4)
		t = datetime.date.today().strftime('%m-%d-%Y')
		print(t)
		update_database(rainfall_allday, t, x['code'])
		
		#rainfall_allday = rainfall_dict['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm'];
		#date = str(rainfall_dict['forecast']['simpleforecast']['forecastday'][0]['date']['day']) + "-" + str(rainfall_dict['forecast']['simpleforecast']['forecastday'][0]['date']['month']) + "-" + str(rainfall_dict['forecast']['simpleforecast']['forecastday'][0]['date']['year']);
	
		#print(date)
		#document = collection.find_one({'code':x['code']})
		#rainfall_30 = document['rainfall']
		#if(date!=document['date']):
		#	update_database(rainfall_allday,rainfall_30, document['code'],date)
		#else:	
		#	print('already updated!')
	
	#try:	
	#	temp = weather_dict['temp_c']
	#except Exception as exception:
	#	temp = '--'

	#try:	
	#	hum = weather_dict['relative_humidity']
	#except Exception as exception:
	#	hum = '--'

	#try:	
	#	rad = weather_dict['davis_current_observation']['solar_radiation']
	#except Exception as exception:
	#	rad = '--'

	#try:
	#	rain = weather_dict['davis_current_observation']['rain_day_in']
	#except Exception as exception:
	#	rain = '--'

	#last_updated = weather_dict['observation_time_rfc822']
	
	#update_database(data,temp,hum,rad,rain,last_updated)


	
def main():
	data = [
		{
			"Location": "IPB Los Baños, Laguna",
			"Code": "ICALABAR18",
			"DeviceId": "001D0AF11A4F",
			"OwnerPass": "uplbs4r41vc1" 
		},
		{
			"Location": "ISU Cabagan, Isabela",
			"Code": "ICAGAYAN3",
			"DeviceId": "001D0AF11A50",
			"OwnerPass": "uplbs4r41vc2"
		},
		{
			"Location": "ISU Echague, Isabela",
			"Code": "ICAGAYAN2",
			"DeviceId": "001D0AF11A51",
			"OwnerPass": "uplbs4r41vc3"
		},
		{
			"Location": "CLSU Muñoz, Nueva Ecija",
			"Code": "ICENTRAL91",
			"DeviceId": "001D0AF11A52",
			"OwnerPass": "uplbs4r41vc4"
		},
		{
			"Location": "DA-QAES Tiaong, Quezon",
			"Code": "ICALABAR25",
			"DeviceId": "001D0AF11A55",
			"OwnerPass": "uplbs4r41vc5"
		},
		{
			"Location": "WVSU Lambunao, Iloilo",
			"Code": "IWESTERN635",
			"DeviceId": "001D0AF11A77",
			"OwnerPass": "uplbs4r41vc6"
		},
		{
			"Location": "CTU Barili, Cebu",
			"Code": "ICENTRAL94",
			"DeviceId": "001D0AF11A57",
			"OwnerPass": "uplbs4r41vc7"
		},
		{
			"Location": "BUCAF Guinobatan, Albay",
			"Code": "IBICOLGU2",
			"DeviceId": "001D0AF11A7C",
			"OwnerPass": "uplbs4r41vc8"
		},
		{
			"Location": "WPU Aborlan, Palawan",
			"Code": "IMIMAROP6",
			"DeviceId": "001D0AF11A7E",
			"OwnerPass": "uplbs4r41vc9"
		},
		{
			"Location": "MinSCAT Victoria, Oriental Mindoro",
			"Code": "IMIMAROP7",
			"DeviceId": "001D0AF11A7F",
			"OwnerPass": "uplbs4r41vc10"
		},
		{
			"Location": "PhilRice Sta. Cruz, Occidental Mindoro",
			"Code": "IMIMAROP8",
			"DeviceId": "001D0AF11A58",
			"OwnerPass": "uplbs4r41vc11"
		},
		{
			"Location": "PCA Zamboanga, Zamboanga del Sur",
			"Code": "IZAMBOAN4",
			"DeviceId": "001D0AF11A81",
			"OwnerPass": "uplbs4r41vc12"
		},
		{
			"Location": "SPAMAST Matanao, Davao del Sur",
			"Code": "IDAVAORE19",
			"DeviceId": "001D0AF11D7F",
			"OwnerPass": "uplbs4r41vc13"
		},
		{
			"Location": "SPAMAST Malita, Davao del Sur",
			"Code": "IDAVAORE20",
			"DeviceId": "001D0AF11A59",
			"OwnerPass": "uplbs4r41vc14"
		},
		{
			"Location": "CMU Maramag, Bukidnon",
			"Code": "INORTHER117",
			"DeviceId": "001D0AF11D80",
			"OwnerPass": "uplbs4r41vc15"
		},
		{
			"Location": "USTP Claveria, Misamis Oriental",
			"Code": "INORTHER86",
			"DeviceId": "001D0AF11A5D",
			"OwnerPass": "uplbs4r41vc16"
		},
		{
			"Location": "USM Kabacan, North Cotabato",
			"Code": "IREGIONX6",
			"DeviceId": "001D0AF11A5A",
			"OwnerPass": "uplbs4r41vc17"
		},
		#{
		#	"Location": "UPLB-CA LGRTS La Carlota, Negros Occidental",
		#	"Code": "IWESTERN596",
		#	"DeviceId": "001D0AF11D82",
		#	"OwnerPass": "uplbs4r41vc18"
		#},
		{
			"Location": "NCAS Los Baños, Laguna",
			"Code": "ILOSBAOS2",
			"DeviceId": "001D0AF11D84",
			"OwnerPass": "uplbs4r41vc20"
		}
    	]
	
	#for d in data:
	get_weather_data()

if __name__ == "__main__":
    main()





