import requests
from bs4 import BeautifulSoup
import pandas

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://omsk.mlsn.ru/arenda-nedvizhimost/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")
data = soup.find_all("div", class_="flex-item__container")

# создаем список словарей с данными
data_list = []
for i in data:
    address = i.find("a", class_="location slim").text
    price = i.find("div", class_="property__price").text
    area = i.find("div", class_="property__area").text
    building = i.find("div", class_="property__building").text
    description = i.find("div", class_="properties__description").text
    card_url = i.find("a", class_="location slim").get("href")

    # добавляем данные в список словарей
    data_list.append({
        "address": address,
        "price": price,
        "area": area,
        "building": building,
        "description": description,
        "card_url": card_url,
    })

# создаем датафрейм из списка словарей
df = pd.DataFrame(data_list)

# записываем датафрейм в файл Excel
df.to_excel("real_estate.xlsx", index=False)
