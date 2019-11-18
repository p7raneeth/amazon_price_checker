# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 11:42:53 2019

@author: praneeth krishna
"""
import requests
from bs4 import BeautifulSoup as bs
import re
import smtplib
import json
import time


def extract_price(soup):
    """ extract price of a product on amazon india website"""
    price = soup.find(id='soldByThirdParty').get_text()
    price_conv = ''.join(re.findall(r'\d+', price)[:-1])
    return int(price_conv)


def extract_average_rating_value(soup):
    """ this function extracts all the avg rating value and the total number of ratings given"""
    rating = soup.find('span', {"class" : "reviewCountTextLinkedHistogram noUnderline"})
    rating = float(rating.find('i').get_text().split(' ')[0])
    rev_cnt = soup.find(id='acrCustomerReviewText').get_text()
    rev_cnt = ''.join(re.findall(r'\d+', rev_cnt))
    return rating, rev_cnt


def extract_user_comments(soup):
    """ extracts user comments for a product"""
    reviews = soup.find_all(id="cm-cr-dp-review-list")
    return reviews


def send_email(username, passkey, URL, recipient):
    "sends mail to the user"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, passkey)
    subject = 'price has been shooted'
    body = URL
    msg = f"subject\n\n:{subject}\ncheck the below link \n{body}"
    server.sendmail(username, recipient, msg)
    print('Email has been sent!!')
    server.quit()


if __name__ == "__main__":
    URL = 'https://www.amazon.in/Uncharted-The-Lost-Legacy-PS4/dp/B01LTI9IEA/ref=sr_1_1?keywords=the+lost+legacy+ps4&qid=1574100196&s=electronics&sr=1-1-catcorr'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    with open('creds_config.txt') as json_file:
        data = json.load(json_file)
    username, passkey, recipient = data['username'], data['passkey'], data['senders']
    page = requests.get(URL, headers=headers)
    soup = bs(page.content, 'html.parser')
    avg_rating, no_of_ratings = extract_average_rating_value(soup)
    reviews = extract_user_comments(soup)
    while(True):
        price_conv = extract_price(soup)
        if price_conv < 320:
            send_email(username, passkey, URL, recipient)
        time.sleep(100)

        