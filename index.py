import requests
from bs4 import BeautifulSoup
import smtplib
import time
import os
from dotenv import load_dotenv
load_dotenv()


URL = "https://www.amazon.com/Apple-MacBook-13-inch-256GB-Storage/dp/B08N5M7S6K/ref=sr_1_4?crid=1VRER76BM35QG&keywords=macbook+air&qid=1654541140&sprefix=macbook+ai%2Caps%2C167&sr=8-4"
headers = {"user-agent": os.getenv('USER_AGENT')}

page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
title = soup.find(id="productTitle").get_text().strip()
price = soup.find(id="priceblock_ourprice").get_text().strip()
itemFound = False


def sendMail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("michaelshahidi@gmail.com", os.getenv('HASH'))

    subject = title + " Price Drop!!!"
    body = "Here is the link to your product: {} \n Enjoy!".format(
        URL)
    msg = "Subject: {}\n\n{}".format(subject, body)
    server.sendmail(
        'michaelshahidi@gmail.com', 'michaelshahidi@gmail.com', msg
    )
    print("Hello! The price has lowered!")
    server.quit()


def checkPrice():
    global itemFound
    priceInNumeric = float(price[1:])
    print("checking price")
    if(priceInNumeric < 900):
        sendMail()
        itemFound = True


while(not itemFound):
    checkPrice()
    time.sleep(86400)
