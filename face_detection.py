#! /usr/bin/python3
import http.client
import urllib.request
import urllib.parse
import urllib.error
import json
from settings import face_api_key
import sys


def face_detection(url_from_argument):
    headers = {
        'Content-Type': 'Application/json',
        'Ocp-Apim-Subscription-Key': face_api_key,
    }

    params = urllib.parse.urlencode({
        'returnFaceId': 'false',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,smile',
    })
    body = {'url': url_from_argument}
    print(body)
    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/detect?%s" %
                     params, json.dumps(body), headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        json_data = json.loads(data)
        age = json_data[0]['faceAttributes']['age']
        gender = json_data[0]['faceAttributes']['gender']
        smile = json_data[0]['faceAttributes']['smile']
        return age, gender, smile
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
print(face_detection(sys.argv[1]))
