import requests
from bs4 import BeautifulSoup

def get_weather(place):
    url = 'https://www.google.com/search?&q=weather in ' + place
    req = requests.get(url)
    scrap = BeautifulSoup(req.text, 'html.parser')
    tmp = scrap.find("div", class_="BNeawe").text
    tm = scrap.find("div", class_="BNeawe tAd8D AP7Wnd").text
    tm = tm.replace('\n', ' ').split(' ')
    print('Date & Time is: ' + tm[0] + ' ' + tm[1] + ':' + str(tm[2]).upper())
    print('Weather is: ' + tm[3])
    print('Temprature is: '+tmp)