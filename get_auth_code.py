from fyers_api import accessToken
import configparser
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import urllib.parse as urlparse


# get all required credentials from config.ini file

config = configparser.ConfigParser()
config.read('config.ini')
app_id = config['fyers']['app_id']
app_secret = config['fyers']['app_secret']
redirect_url = config['fyers']['redirect_url']
user_id = config['fyers']['user_id']
password = config['fyers']['password']
two_fa = config['fyers']['two_fa']

# generate the session url
session=accessToken.SessionModel(client_id=app_id, 
                                    secret_key= app_secret,
                                    redirect_uri= redirect_url, 
                                    response_type='code', 
                                    grant_type='authorization_code')
session_url =  session.generate_authcode() 

# to automate the login procedure, I have used selenium webdriver
# launch firefox  driver
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Firefox(executable_path=r'geckodriver.exe', options=options)
driver.get(session_url)


# initiate longin

xpath = ["//*[@id='fy_client_id']", "//*[@id='fy_client_pwd']"]
keys = [user_id, password]

for i in range(2):
    driver.find_element(by= By.XPATH, value= xpath[i]).send_keys(keys[i])
    sleep(1)
    driver.find_element(by= By.XPATH, value= xpath[i]).submit()
    sleep(1)

for i in range(4):
    digit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/section[8]/div[3]/div[3]/form/div[2]/input[{}]".format(i+1))))
    digit.send_keys(two_fa[i])
    sleep(0.1)

submit = WebDriverWait(driver, 20).until(lambda x: x.find_element(By.XPATH,"//*[@id='verifyPinSubmit']"))
submit.click()
sleep(2)

# login successful
# get the authorization code

current_url = driver.current_url
driver.close()
parsed = urlparse.urlparse(current_url)
auth_code = urlparse.parse_qs(parsed.query)['auth_code'][0]

print(auth_code)