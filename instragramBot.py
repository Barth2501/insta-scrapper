from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from utils import main as bald_detector
import time
import random
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
        time.sleep(1+random.randint(0,200)/100)

    def search_for_tags(self, tag, limit, begin):
        self.browser.get('https://www.instagram.com/explore/tags/{}/'.format(tag))
        time.sleep(1+random.randint(0,200)/100)
        print('begin scrap')
        post = 'https://www.instagram.com/p/'
        df = pd.read_csv('./output/profile_to_follow.csv')
        res = {}
        res['profile'] = []
        res['picture'] = []
        seen = []
        loop = 0
        while len(res['profile'])<limit:
            links = [a.get_attribute('href') for a in self.browser.find_elements_by_tag_name('a')]
            print(len(links))
            for i,link in enumerate(links):
                print(i)
                # permet d'eviter les post 'meilleures publications' et permet d'eviter de chercher les a tag du bas de page qui ne sont pas des posts
                if loop==0 and i>18 and i<len(links)-15:
                    # loop*30 sert a ne pas rescrapper tous les profiles vu précédemment, le 40 est a modifer car pas sur que ce soit le nombre exact de 
                    # post qui s'ouvre lors du scroll down
                    if post in link and link not in seen and i>=loop*40:
                        seen.append(link)
                        self.browser.get(link)
                        print('accessing post')
                        time.sleep(1+random.randint(0,100)/100)
                        profile_url = self.browser.find_elements_by_tag_name('a')[0].get_attribute('href')
                        if profile_url not in seen:
                            seen.append(profile_url)
                        self.browser.get(profile_url)
                        print('accessing profile')
                        time.sleep(1+random.randint(0,100)/100)
                        image_url=self.browser.find_elements_by_css_selector('div.XjzKX img')[0].get_attribute('src')
                        try:
                            profile_username=self.browser.find_elements_by_css_selector('section.zwlfE > div > h2')[0].text
                        except:
                            profile_username=self.browser.find_elements_by_css_selector('section.zwlfE > div > h1')[0].text
                        is_bald = bald_detector(image_url)
                        print(is_bald)
                        if is_bald==True:
                            res['profile'].append(profile_username)
                            res['picture'].append(image_url)
                            df = df.append({'profile_name':profile_username, 'picture':image_url},ignore_index=True)
                            df.to_csv('./output/profile_to_follow.csv', index=False)
                            print(res)
            loop+=1
            self.browser.get('https://www.instagram.com/explore/tags/{}/'.format(tag))
            scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
            for _ in range(loop):
                self.browser.execute_script(scroll_down)
                time.sleep(random.randint(2,5)/10)
            time.sleep(1+random.randint(0,200)/100)
        return res

        