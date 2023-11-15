import json
import requests
import smtplib
import time
from datetime import datetime

# import private data
with open('priv.json') as f:
    priv = json.load(f)
    my_email = priv["email"]
    app_pass = priv["app_pass"]
    smtp_address = priv["smtp_address"]
    mail_to = priv["mail_to"]
    MY_LAT = priv["MY_LAT"]  # Your latitude
    MY_LNG = priv["MY_LNG"]  # Your longitude


def iss_overhead():
    resp = requests.get(url="http://api.open-notify.org/iss-now.json")
    resp.raise_for_status()
    data_iss = resp.json()
    iss_latitude = float(data_iss["iss_position"]["latitude"])
    iss_longitude = float(data_iss["iss_position"]["longitude"])
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LNG - 5 <= iss_longitude <= MY_LNG + 5:
        return True


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0
    }
    resp = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    resp.raise_for_status()
    data_sun = resp.json()
    sunrise = int(data_sun["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data_sun["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now <= sunrise or time_now >= sunset:
        return True


check_iss = True
while check_iss:
    time.sleep(60)
    if iss_overhead() and is_dark():
        with smtplib.SMTP(smtp_address) as connection:
            connection.starttls()
            connection.login(user=my_email, password=app_pass)
            connection.sendmail(from_addr=my_email,
                                to_addrs=mail_to,
                                msg="Subject:Look Up ☝\n\nThe international space station 🛰 is over your head!!!")
        # check_iss = False
