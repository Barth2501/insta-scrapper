from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from utils import main as bald_detector
import time
import pandas as pd
import gc


class InstagramBot():

    def __init__(self, username, pwd):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.username = username
        self.pwd = pwd

    def login(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
            "input[name='username']")))
        emailInput = self.browser.find_elements_by_css_selector('form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

        emailInput.send_keys(self.username)
        passwordInput.send_keys(self.pwd)
        passwordInput.send_keys(Keys.ENTER)
        print('logged in')
        time.sleep(2)

    def search_for_tags(self, tag, limit, begin):
        self.browser.get('https://www.instagram.com/explore/tags/{}/'.format(tag))
        time.sleep(5)
        print('begin scrap')
        post = 'https://www.instagram.com/p/'
        df = pd.read_csv('./output/profile_to_follow.csv')
        res = {}
        res['profile'] = []
        res['picture'] = []
        seen = []
        loop = 0
        while len(res['profile'])<limit:
            if loop>=5:
                links = [a.get_attribute('href') for a in self.browser.find_elements_by_tag_name('a')]
                for i,link in enumerate(links):
                    if post in link and link not in seen and i>=begin:
                        seen.append(link)
                        self.browser.get(link)
                        print('accessing post')
                        time.sleep(5)
                        profile_url = self.browser.find_elements_by_tag_name('a')[0].get_attribute('href')
                        self.browser.get(profile_url)
                        print('accessing profile')
                        time.sleep(5)
                        image_url=self.browser.find_elements_by_css_selector('div.XjzKX img')[0].get_attribute('src')
                        profile_username=self.browser.find_elements_by_css_selector('section.zwlfE > div > h2')[0].text
                        is_bald = bald_detector(image_url)
                        print(is_bald)
                        if is_bald==True:
                            res['profile'].append(profile_username)
                            res['picture'].append(image_url)
                            df = df.append({'profile_name':profile_username, 'picture':image_url},ignore_index=True)
                            df.to_csv('./output/profile_to_follow.csv', index=False)
                            print(res)
                        ## try to release memory
                        gc.collect()
            loop+=1
            scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
            self.browser.execute_script(scroll_down)
            time.sleep(5)
        return res