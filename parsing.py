import pandas as pd
from bs4 import BeautifulSoup
import requests
import lxml


url = 'https://www.mr-group.ru/catalog/apartments/?project=45589&project_type=apartments&view_mode=list&building%5B%5D=all&floor%5B%5D=all&renovation%5B%5D=all&availability_renovation=all&sort=PROPERTY_IS_ENABLED_DESC&page=1'
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")
house_data = soup.find_all('div', class_ = 'catalog-item__wrap')

home = {'Площадь': [],
        'Этаж': [],
        'Цена': [],
        'Цена за Квадратный метр': [],
        'Кол-во комнат': [],
        'Корпус': []
       }

for flat in house_data:
    home['Площадь'].append(flat.find_all("div", class_ = "catalog-item__title _hover")[2].text.split()[2])
    home['Этаж'].append(flat.find_all("div", class_ = "catalog-item__title _hover")[1].text.replace(" этаж", ''))
    home['Цена'].append(int(flat.find("div", class_ = "catalog-item__title _price _hover").text[:-1].replace('\xa0', '')))
    home['Цена за Квадратный метр'].append(int(flat.find("div", class_ = "catalog-item__subtitle _area").text.replace('\xa0', '').split()[0]))
    home['Кол-во комнат'].append(flat.find_all("div", class_ = "catalog-item__title _hover")[2].text.split()[0])
    home['Корпус'].append(flat.find_all("div", class_ = "catalog-item__title _hover")[0].text)

data = pd.DataFrame(home)
print(data)