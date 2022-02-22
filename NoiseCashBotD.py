from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from apscheduler.schedulers.blocking import BlockingScheduler
import re

class NCBot:
    def __init__(self, email, password):
        self.driver = webdriver.Chrome(executable_path = '/Users/jen/bin/chromedriver')
        self.email = email
        self.password = password
    def CopyTweet(self, topic):
        url = "https://twitter.com/search?q=" + topic + "&f=live"
        self.driver.get(url)
        time.sleep(5)
        tweets = self.driver.find_elements_by_css_selector("[data-testid=\"tweet\"]")
        ifPost = 0
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
                break
        postNC = '\n'.join(str2[dotPosition+2:])
        return postNC
    def Login(self):
        urlLogin = "https://noise.cash/login"
        self.driver.get(urlLogin)
        time.sleep(3)
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
    emails = ["Acct1@gmail.com", "Acct2@gmail.com", "ACCT3@yandex.com"]
    email = random.choice(emails)
    pw = "password"                       ## password
    Bot = NCBot(email, pw)
    print("I am " + email)
    try:
        postNC = Bot.CopyTweet("vtuber")  ## copy topic
    except:
        postNC = '0'
    Bot.Login()
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
        postNC = re.sub(r'\b@', '', postNC)
        postNC = re.sub(r'\b#', '', postNC)
        # print(postNC)
        Bot.Post(postNC)
    Bot.Close()

# job_task()
scheduler = BlockingScheduler()
scheduler.add_job(job_task, 'interval', minutes=15)
scheduler.start()
