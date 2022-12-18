#Dotproperty - Bangkok - rent
import datetime
import bs4
import requests
import time
import mysql.connector

page = 1
url = "https://www.dotproperty.co.th/condos-for-rent/bangkok?sort=newest&page=" + str(page)
name_list = []
price_list = []
location_list = []
url_list = []
while page <= 3 :
      url = "https://www.dotproperty.co.th/condos-for-rent/bangkok?sort=newest&page=" + str(page)
      data = requests.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36'})
      data.encoding = "utf-8"
      data_get = bs4.BeautifulSoup(data.text, 'html.parser')
      place_data = data_get.find_all('div', {'class': 'wrapper'})
      dict_place = {}
      storage = ""
      for i in place_data:
            name = i.find('h3', {'class': 'name'}).text.strip()
            name_list.append(name)
            price = i.find('div', {'class': 'price'}).text.replace('฿ ','').replace(' / เดือน\nNew listing','').replace(',','').strip()
            price_list.append(price)
            location = i.find('div', {'class': 'location'}).text.replace('\n',',').strip()
            location = location.replace(', ',' ').split()[0].replace(',','')
            location_list.append(location)
            url = i.find("a",{'target':'_blank'}).get('href').rstrip().replace(" ","")
            url_list.append(url)

      print("PAGE "+str(page)+" SCRAPED!!!")
      page += 1

item_count = len(name_list)

con = mysql.connector.connect(
    host = "localhost",
    user = "root",
    db = "myscraping"
)

cursorpy = con.cursor()
for i in range(item_count) :
    date_now = datetime.datetime.now()
    query = "INSERT INTO condodb (Name,Price,Location,Url,DateAdd) VALUES (%s , %s , %s ,%s, %s)"
    vaule = (name_list[i],int(price_list[i]),location_list[i],url_list[i],date_now)
    cursorpy.execute(query , vaule)

con.commit()
print(cursorpy)