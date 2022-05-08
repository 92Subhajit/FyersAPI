import configparser
from fyers_api import fyersModel
from fyers_api import accessToken
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import urllib.parse as urlparse
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
from datetime import date

import pandas as pd

class Fyers:
    def __init__(self, app_id, app_secret, redirect_url,user_id, password, two_fa):
        self.app_id = app_id
        self.app_secret = app_secret
        self.redirect_url = redirect_url
        self.user_id = user_id
        self.password = password
        self.two_fa = two_fa
        self.string = ' ********** '
    
    def print_message(self,msg):
        return print(self.string + msg + self.string)

    def get_session_url(self):
        self.session=accessToken.SessionModel(client_id=self.app_id, 
                                        secret_key=self.app_secret,
                                        redirect_uri=self.redirect_url, 
                                        response_type='code', 
                                        grant_type='authorization_code')
        self.url = self.session.generate_authcode() 
    
    def login_driver(self):
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            driver = webdriver.Firefox(executable_path=r'geckodriver.exe', options=options)
            driver.get(self.url)
            
            xpath = ["//*[@id='fy_client_id']", "//*[@id='fy_client_pwd']"]
            keys = [self.user_id, self.password]

            for i in range(2):
                driver.find_element(by= By.XPATH, value= xpath[i]).send_keys(keys[i])
                sleep(1)
                driver.find_element(by= By.XPATH, value= xpath[i]).submit()
                sleep(1)

            for i in range(4):
                digit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/section[8]/div[3]/div[3]/form/div[2]/input[{}]".format(i+1))))
                digit.send_keys(self.two_fa[i])
                sleep(0.1)

            submit = WebDriverWait(driver, 20).until(lambda x: x.find_element(By.XPATH,"//*[@id='verifyPinSubmit']"))
            submit.click()
            sleep(2)
            self.print_message('Login Successful')
            return driver
        except:
            self.print_message('Login Unsuccessful')
        

    def get_auth_code(self,driver):
        try:
            current_url = driver.current_url
            parsed = urlparse.urlparse(current_url)
            auth_code = urlparse.parse_qs(parsed.query)['auth_code'][0]
            driver.close()
            self.print_message('Authentication code generated')
            return auth_code
        except:
            pass
    def set_token(self):
        try:
            self.get_session_url()
            driver = self.login_driver()
            auth_code = self.get_auth_code(driver)
            self.session.set_token(auth_code)
            self.print_message('Authentication code validated')
            response = self.session.generate_token()
            access_token = response['access_token']
            self.print_message('Access token generated')
            self.fyers = fyersModel.FyersModel(client_id=self.app_id, token=access_token,log_path="\log")
        except:
            pass

    def get_historical_data(self, symbol, resolution, startdate, enddate):            
        data = {"symbol": symbol,"resolution":resolution,"date_format":"1","range_from": startdate.strftime( "%Y-%m-%d"),"range_to":enddate.strftime( "%Y-%m-%d"),"cont_flag":"1"}
        data = self.fyers.history(data)
        col = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        price_data = pd.DataFrame(data['candles'], columns= col)
        del data
        price_data['Date'] = pd.to_datetime(price_data['Date'],unit='s')
        price_data = price_data.set_index('Date')
        return price_data