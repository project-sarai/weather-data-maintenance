#!/usr/bin/python3
from pymongo import MongoClient
import urllib3
import json
import reverse_geocoder as rg

mongodb_host = 'localhost'
mongodb_port = '3001' #change port depending on database
client  = MongoClient(mongodb_host + ':' + mongodb_port)
db = client['meteor'] #change according to the db name
collection = db['seams-gallery']
province_collection = db['seams-provinces']

http = urllib3.PoolManager()

def updateProvinces(provinces_dict):
    provinces = []
    for key in provinces_dict.keys():
        provinces.append({
            'province':key,
            'municipality': list(provinces_dict[key].keys())
        })
    
    province_collection.remove({})
    x = province_collection.insert_many(provinces)
    print(provinces)


def updateDatabase(seamsGallery):
    collection.remove({})
    x = collection.insert_many(seamsGallery)
    print(x)
    

def getData():
    api = "https://firestore.googleapis.com/v1beta1/projects/seams-image-caputring/databases/(default)/documents/post?pageToken="
    seamsGallery = []
    token = ""
    index = 1
    provinces = {}
    while True:
        api = "https://firestore.googleapis.com/v1beta1/projects/seams-image-caputring/databases/(default)/documents/post?pageToken=" + token
        response = http.request('GET',api)
        seamsData = json.loads(response.data.decode('UTF-8'))
        for data in seamsData['documents']:
            coordinates = (data['fields']['coords']['arrayValue']['values'][0]['doubleValue'], data['fields']['coords']['arrayValue']['values'][1]['doubleValue'])
            reverseGeocode = rg.search(coordinates)

            if reverseGeocode[0]['admin2'] not in provinces.keys():
                provinces[reverseGeocode[0]['admin2']] = {}    

            provinces[reverseGeocode[0]['admin2']][reverseGeocode[0]['name']] = 1

            seamsGallery.append({
                'coords': {
                    'lat' : data['fields']['coords']['arrayValue']['values'][0]['doubleValue'],
                    'long' : data['fields']['coords']['arrayValue']['values'][1]['doubleValue']
                },
                'createTime': data['createTime'],
                'updateTime': data['updateTime'],
                'firstName' : data['fields']['first_name']['stringValue'],
                'lastName' : data['fields']['last_name']['stringValue'],
                'contact' : data['fields']['contact']['stringValue'],
                'purpose' : data['fields']['purpose']['stringValue'],
                'stage' : data['fields']['stage']['stringValue'],
                'crop' : data['fields']['crop']['stringValue'],
                'title': data['fields']['title']['stringValue'] if ('title' in data['fields'].keys()) else '',
                'description' : data['fields']['description']['stringValue'],
                'imageUrl' : data['fields']['imageUrl']['stringValue'],
                'province' : reverseGeocode[0]['admin2'],
                'municipality' : reverseGeocode[0]['name'],
                'fileName' : str(index) + '.jpeg'
            })
            index += 1

        print(len(seamsGallery))

        if 'nextPageToken' not in seamsData.keys():
            break
        
        token = seamsData['nextPageToken']

    updateProvinces(provinces)
    return seamsGallery


def main():
    seamsGallery = getData()
    updateDatabase(seamsGallery)


if __name__ == "__main__":
    main()
