#!/usr/bin/python3
from pymongo import MongoClient
import urllib3
import json

mongodb_host = 'localhost'
mongodb_port = '3001' #change port depending on database
client  = MongoClient(mongodb_host + ':' + mongodb_port)
db = client['meteor'] #change according to the db name
collection = db['seams-gallery']

http = urllib3.PoolManager()

def updateDatabase(seamsGallery):
    collection.remove({})
    x = collection.insert_many(seamsGallery)
    print(x)
    

def getData():
    api = "https://firestore.googleapis.com/v1beta1/projects/seams-image-caputring/databases/(default)/documents/post?pageToken="
    seamsGallery = []
    token = ""
    while True:
        api = "https://firestore.googleapis.com/v1beta1/projects/seams-image-caputring/databases/(default)/documents/post?pageToken=" + token
        response = http.request('GET',api)
        seamsData = json.loads(response.data.decode('UTF-8'))
        for data in seamsData['documents']:
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
            })

        print(len(seamsGallery))

        if 'nextPageToken' not in seamsData.keys():
            break
        
        token = seamsData['nextPageToken']

    return seamsGallery


def main():
    seamsGallery = getData()
    updateDatabase(seamsGallery)


if __name__ == "__main__":
    main()
