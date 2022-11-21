from module.scraper import Insta
from setting.setting import USERNAME,PASSWORD,Config
import requests
import random


def main():
    
    ig = Insta(USERNAME,PASSWORD,timeout=30, browser='chrome', headless=True)

    ig.is_page_loaded()

    ig.login()

    ig.dont_save_login_info()

    is_login = ''
    try:
        ig.validate_login()

        is_login = 'success login'
    
    except:
        is_login = 'failed'

    print(is_login)

    headers_list = Config.userAgent()
        #menambahkan user agent
    userA = random.choice(headers_list)

    cookie     = ig.cookie()

    cok = ''
    for key in cookie:
        cok += f"{key['name']} = {key['value']};" 

        if key['name'] == 'csrftoken':

            csrf = key['value']
    
    url_profile = "https://www.instagram.com/api/v1/web/search/topsearch/?query=sales%20honda"
    
    payload={}
    headers = {
    'Cookie': cok
    }

    response = requests.request("GET", url_profile, headers=headers, data=payload)

    users_list = response.json()
    
    print(cok)
    for row in users_list['users']:
        print(row['user']['username'])
        info = "https://www.instagram.com/api/v1/users/web_profile_info/?username="+row['user']['username']
        
        test = f"https://www.instagram.com/{row['user']['username']}/"

        d = ig.fetch_userAgent(test)

        pay={}
        head = {
            'Cookie': cok,
            'X-CSRF-Token':csrf,
            'User-Agent': d,
            'X-IG-App-ID':'936619743392459'
           }

        res = requests.get(info, headers=head, data=pay)

        hasil = res.json()

        try:
            profile =hasil['data']['user']['biography']
        except:
            profile = 'N/A'

        print(profile)

if __name__ == "__main__":
    main()