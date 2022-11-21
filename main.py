from module.scraper import Insta
from setting.setting import USERNAME,PASSWORD

def main():

    ig = Insta(USERNAME,PASSWORD,timeout=30, browser='chrome', headless=False)

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

    user_agent = ig.fetch_userAgent()

    cookie     = ig.get_cookie()

    ig.btn_search()

if __name__ == "__main__":
    main()