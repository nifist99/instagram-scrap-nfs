from module.scraper import Insta
from setting.setting import Config
import requests
import random

from api.api_web import Api
import undetected_chromedriver.v2 as uc

def main():


    print('#*********** INI ADALAH METODE SCRIPT INSTAGRAM ***************#')
    
    print("")

    code   = input('masukan code scryping check di website =') 

    result = Api.setting(code)

    if result['status'] == 'success':
        s = str(result['search'])
        search = s.replace(' ','%20')

        print(search)

        ig = Insta(result['username'],result['sandi'],timeout=30, browser='chrome', headless=False)

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
        
        url_profile = "https://www.instagram.com/api/v1/web/search/topsearch/?query="+search
        
        payload={}
        headers = {
        'Cookie': cok
        }

        response = requests.request("GET", url_profile, headers=headers, data=payload)

        users_list = response.json()
        
        print(cok)

        print("")

        for row in users_list['users']:
            print(row)
            print(row['user']['username'])
            check_db = Api.check(row['user']['username'])

            if check_db['status'] == 'failed':
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
                    num = ""
                    stf = str(hasil['data']['user']['biography'])
                    for c in stf:
                        if c.isdigit():
                            num = num + c

                except:
                    num ='na'

                try:
                    saves = {
                                'instagram_id'            :result['id'],
                                'bio'                     :hasil['data']['user']['biography'],
                                'id_ig'                   :hasil['data']['user']['id'],
                                'business_category_name'  :hasil['data']['user']['business_category_name'],
                                'username'                :hasil['data']['user']['username'],
                                'external_url'            :hasil['data']['user']['external_url'],
                                'external_url_linkshimmed':hasil['data']['user']['external_url_linkshimmed'],
                                'full_name'               :hasil['data']['user']['full_name'],
                                'profile_pic_url'         :hasil['data']['user']['profile_pic_url'],
                                'email'                   :'N/A',
                                'phone'                   : num,
                            }
                    t=Api.save(saves)
                    print(t)

                except:
                    profile = 'N/A'
            
            else:

                print("data sudah ada")

        

if __name__ == "__main__":
    main()