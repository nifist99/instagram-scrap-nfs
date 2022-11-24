import requests
import json

base_url = 'http://127.0.0.1:8000/api'

class Api:

    def setting(code):
        try:
            url = f'{base_url}/instagram/code/{code}'

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            r = response.json()

            return r
        except:
            return Api.setting(code)

    
    def check(username):
        try:
            url = f'{base_url}/instagram/check/{username}'

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            r = response.json()

            return r
        except:
            return Api.check(username)

    
    def save(key):
        try:
                url = f"{base_url}/instagram/save"
                payload = json.dumps({
                    "instagram_id"              : key['instagram_id'],
                    "bio"                       : key['bio'],
                    "id_ig"                     : key['id_ig'],
                    "business_category_name"    : key['business_category_name'] ,
                    "username"                  : key['username'],
                    "external_url"              : key['external_url'],
                    "external_url_linkshimmed"  : key['external_url_linkshimmed'],
                    "full_name"                 : key['full_name'],
                    "profile_pic_url"           : key['profile_pic_url'],
                    "email"                     : key['email'],
                    "phone"                     : key['phone'],
                })
                headers = {
                'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(key['nama'])
                print('save profile api run')
                return response.json()

        except:
            return "wait" 