import requests
import os
from twilio.rest import Client

api_key = os.environ['OPEN_WEATHER_API_KEY']
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

parameters = {
    "lat": 49.900501,
    "lon": -97.139313,
    "appid": api_key,
    "exclude": "current,minutely,daily",
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()
data=response.json()
weather_id = data["hourly"][0]["weather"][0]["id"]
next_twelve_hours = data["hourly"][:12]

will_rain = False

for data in next_twelve_hours:
    condition_code = data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain, bring an umbrella!",
        from_=os.environ['TWILIO_PHONE_NUMBER'],
        to=os.environ['PHONE_NUMBER']
    )
    print(message.status)

