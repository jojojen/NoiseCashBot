from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
from deep_translator import GoogleTranslator

def copyTweet(topic):
    url = "https://twitter.com/search?q=" + topic + "&f=live"
    driver = webdriver.Chrome(executable_path = '/Users/jen/bin/chromedriver')
    driver.get(url)
    time.sleep(5)
    try:
        tweets = driver.find_elements_by_css_selector("[data-testid=\"tweet\"]")
    except:
        driver.get(url)
        time.sleep(5)
        tweets = driver.find_elements_by_css_selector("[data-testid=\"tweet\"]")
    postNC = '0'
    for tweet in tweets:
        str1 = tweet.text
        str2 = str1.split('\n')
        isReply = 0
        for elem in str2:
            if elem == '回覆給 ' or elem == '回覆 ':
                isReply = 1
                break
        if isReply == 0:
            dotPosition = str2.index('·')
            post = '\n'.join(str2[dotPosition+2:])
            break
    driver.close()
    return post

def getProxy():
    url = "https://www.us-proxy.org"
    driver = webdriver.Chrome(executable_path = '/Users/jen/bin/chromedriver')
    driver.get(url)
    IPPool = []
    url = 'http://free-proxy.cz/zh/proxylist/country/US/https/ping/all/{}'.format(1)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source)
    for j in soup.select('tbody > tr'):
        if re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', str(j)):
            IP = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', str(j))[0]
            Port = re.findall('class="fport" style="">(.*?)</span>', str(j))[0]
            IPPool.append(pd.DataFrame([{'IP':IP, 'Port':Port}]))
    IPPool = pd.concat(IPPool, ignore_index=True)
    driver.close()
    ActIps = []
    act_nums = 0
    for i in range(len(IPPool)):
        proxy = {'https':'https://'+ IPPool["IP"][i] + ':' + IPPool["Port"][i]}
        try:
            if act_nums < 3:
                url = 'https://noise.cash'
                resp = requests.get(url, proxies=proxy, timeout=2)
                if str(resp.status_code) == '200':
                    ActIps.append(IPPool["IP"][i] + ':' + IPPool["Port"][i])
                    print('Succed:'+ str(IPPool["IP"][i]) + ":" + str(IPPool["Port"][i]))
                    act_nums += 1
        except:
            continue
    return ActIps

class NCBot:
    def __init__(self, email, password, PROXY):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        self.driver = webdriver.Chrome(executable_path = '/Users/jen/bin/chromedriver', options=chrome_options)
        self.email = email
        self.password = password

    def Login(self):
        urlLogin = "https://noise.cash/login"
        self.driver.get(urlLogin)
        time.sleep(8)
        # driver.set_page_load_timeout(5)
        element = self.driver.find_element_by_id("email")
        element.send_keys(self.email)
        element = self.driver.find_element_by_id("password")
        element.send_keys(self.password)
        element.send_keys(Keys.ENTER)
        time.sleep(5)
    def Post(self, postContent: str):
        self.postContent = postContent
        postXpath = "/html/body/div/div/main/div/div/div[1]/div/div/textarea"
        element = self.driver.find_element_by_xpath(postXpath)
        element.send_keys(postContent)
        time.sleep(3)
        try:
            postBtnXpath = "/html/body/div/div/main/div/div/div[1]/div/div/div[1]/div[3]/button"
            element = self.driver.find_element_by_xpath(postBtnXpath)
            self.driver.find_element_by_xpath(postBtnXpath).click()
        except:
            postBtnXpath = "/html/body/div/div/main/div/div/div[1]/div/div/div[1]/div[2]/button"
            element = self.driver.find_element_by_xpath(postBtnXpath)
            self.driver.find_element_by_xpath(postBtnXpath).click()
        time.sleep(10)
    def Like(self):
        try:
            btnXpath = "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[8]/button/i"
            self.driver.find_element_by_xpath(btnXpath).click()
        except:
            btnXpath = "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[3]/div[8]/button"
            self.driver.find_element_by_xpath(btnXpath).click()
        time.sleep(1)
    def Close(self):
        btnXpath = "/html/body/div[1]/div/nav/div/div/div[3]/div[2]/div/div[1]/button/div[1]"
        self.driver.find_element_by_xpath(btnXpath).click()
        time.sleep(1)
        btnXpath = "/html/body/div[1]/div/nav/div/div/div[3]/div[2]/div[2]/div[2]/div/div/form/a"
        self.driver.find_element_by_xpath(btnXpath).click()
        self.driver.close()
    def Press(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(5)
    def Tip(self):
        tip = 0
        try:
            btnXpath = "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[3]/div[6]"
            self.driver.find_element_by_xpath(btnXpath).click()
            tip = 1
        except:
            tip = 0
        if tip == 0:
            try:
                btnXpath = "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[3]/div[6]/div/div/div[1]/div/span"
                self.driver.find_element_by_xpath(btnXpath).click()
                tip = 1
            except:
                tip = 0
        if tip == 0:
            try:
                btnXpath = "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[6]/div/div/div[1]/div"
                self.driver.find_element_by_xpath(btnXpath).click()
                tip = 1
            except:
                tip = 0
        time.sleep(2)
        try:
            btnXpath = "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[6]/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]/button"
            self.driver.find_element_by_xpath(btnXpath).click()
        except:
            btnXpath = "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[3]/div[6]/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]/button"
            self.driver.find_element_by_xpath(btnXpath).click()
        time.sleep(2)
        try:
            btnXpath = "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[6]/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]"
            self.driver.find_element_by_xpath(btnXpath).click()
        except:
            btnXpath = "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[3]/div[6]/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]"
            self.driver.find_element_by_xpath(btnXpath).click()
        time.sleep(2)
        try:
            btnXpath = "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[6]/div/div[2]/div[2]/div/div/div/div[6]/div[2]/div/button"
            self.driver.find_element_by_xpath(btnXpath).click()
        except:
            btnXpath = "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[3]/div[6]/div/div[2]/div[2]/div/div/div/div[6]/div[2]/div/button"
            self.driver.find_element_by_xpath(btnXpath).click()
        time.sleep(2)
        print("Give tip")

def job_task():
    ## copy tweet
    try:
        postNC = copyTweet("vtuber")
    except:
        postNC = '0'
    ## get proxy
    proxyList = getProxy()
    ## NoiseCash
    ifLogin = 0
    for proxy in proxyList:
        PROXY = proxy
        emails = ["acct1@gmail.com" "att2@gmail.com", "att3@yandex.com"]
        email = random.choice(emails)
        pw = "passsword"
        Bot = NCBot(email, pw, PROXY)
        print("I am " + email + " by " + PROXY)
        try:
            Bot.Login()
            ifLogin = 1
            print("ifLogin=1")
            break
        except Exception as e:
            print(e)
            continue
    if ifLogin == 1:
        Bot.Press()
        time.sleep(3)
        try:
            Bot.Like()
            print("Like it")
        except:
            print("Like fail")
        try:
            Bot.Tip()
        except:
            Bot.driver.get("https://noise.cash")
            time.sleep(5)
            print("No tips")
        if postNC != '0':
            postNC = re.sub(r'\@\w+', '', postNC)
            postNC = re.sub(r'twitter', '', postNC)
            to_translate = postNC
            translated = GoogleTranslator(source='auto', target='en').translate(to_translate)
            print(postNC)
            Bot.Post(translated)
            print("posted!")
        else:
            print("No post")
        Bot.Close()
        print(time.ctime())
job_task()
# scheduler = BlockingScheduler()
# scheduler.add_job(job_task, 'interval', minutes=15)
# scheduler.start()
