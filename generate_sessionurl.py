from fyers_api import accessToken
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
app_id = config['fyers']['app_id']
app_secret = config['fyers']['app_secret']
redirect_url = config['fyers']['redirect_url']
user_id = config['fyers']['user_id']
password = config['fyers']['password']
two_fa = config['fyers']['two_fa']


session=accessToken.SessionModel(client_id=app_id, 
                                    secret_key= app_secret,
                                    redirect_uri= redirect_url, 
                                    response_type='code', 
                                    grant_type='authorization_code')
session_url =  session.generate_authcode() 

print(session_url)