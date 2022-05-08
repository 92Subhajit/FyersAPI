# FyersAPI
Sample codes to get started with the Fyers API <br>
Fyers API documentation : https://myapi.fyers.in/docs/

## Create App

To create an app, you need to follow the following steps:-

<ol>
    <li> Login to <a href = 'https://api-dashboard.fyers.in/'> API Dashboard </a> </li>
    <li> Click on Create App </li>
    <li> Provide the following details </li>
    <li> App Name </li>
    <li> Redirect URL </li>
    <li> Description (Optional) </li>
    <li> Image (Optional) </li>
</ol>

## File description

<ol>
    <li> config.ini : store all credentials in this file </li>
    <li> generate_sessionurl.py : This code will generate a session URL. This URL will be further use to get the authorization code. </li>
    <li> get_auth_code.py :  To get the authorization code from the session URL, we need to open the session URL and log in to the fyers account every time. This code will automate the process of getting an authorization code. </li>
</ol>

