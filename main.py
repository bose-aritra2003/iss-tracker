import requests
from datetime import datetime
import smtplib
import time

SENDER_MAIL = "world.hello2003@gmail.com"
SENDER_PASSWORD = "123aritra@#$"
RECIPIENT_EMAIL = "hello.world2003@gmail.com"

MY_LAT = 22.572645  # Your latitude
MY_LONG = 88.363892  # Your longitude


def isIssOverhead():
    iss_response = requests.get(url="https://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    data = iss_response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def isSunset():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    sun_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    sun_response.raise_for_status()
    data = sun_response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    current_hour = int(datetime.now().hour)
    if sunset <= current_hour <= sunrise:
        return True


while True:
    time.sleep(60)
    if isIssOverhead() and isSunset():
        with smtplib.SMTP("smtp.gmail.com", port=587) as server:
            server.starttls()
            server.login(user=SENDER_MAIL, password=SENDER_PASSWORD)
            server.sendmail(
                from_addr=SENDER_MAIL,
                to_addrs=RECIPIENT_EMAIL,
                msg="Subject: ISS Tracker\n\nISS is above you! Go out and give it a look!")
