from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml
import random
import time
import os

def parser(url: str, page_start: int, page_count: int, bool_table: bool = True, bool_pictures: bool = True):
    """
    :param url: Ссылка на страницу
    :param page_start: Начальная страница для парсинга
    :param: page_count: Количество страниц для парсинга
    :param: bool_table: Вывести таблицу в виде data_frame
    :param: bool_pictures: Сохранить картинки или нет
    """
    link = 'https://www.mr-group.ru'
    home = {'id_flat': [],
            'Squre': [],
            'Floor': [],
            'Price': [],
            'Price per square': [],
            'Rooms': [],
            'Frame': []
            }

    # папка для хранения картинок
    if bool_pictures:
        name_folder = 'pictures'
        os.mkdir(name_folder)

    id_flat = 1
    for page in range(page_start, page_start + page_count):
        url_page = url + str(page)
        response = requests.get(url_page)
        soup = BeautifulSoup(response.text, "lxml")
        house_data = soup.find_all('div', class_='catalog-item__wrap')

        for flat in house_data:
            home['Squre'].append(flat.find_all("div", class_="catalog-item__title _hover")[2].text.split()[2])
            home['Floor'].append(flat.find_all("div", class_="catalog-item__title _hover")[1].text.replace(" этаж", ''))
            home['Price'].append(
                int(flat.find("div", class_="catalog-item__title _price _hover").text[:-1].replace('\xa0', '')))
            home['Price per square'].append(
                int(flat.find("div", class_="catalog-item__subtitle _area").text.replace('\xa0', '').split()[0]))
            home['Rooms'].append(flat.find_all("div", class_="catalog-item__title _hover")[2].text.split()[0])
            home['Frame'].append(flat.find_all("div", class_="catalog-item__title _hover")[0].text)
            home['id_flat'].append(id_flat)


            #картинки
            if bool_pictures:
                #ссылка на картинку
                url_picture = link + flat.select("img")[0].attrs["data-src"]
                #отправляем запрос на картинку
                img_bytes = requests.get(url_picture).content
                with open(f'{name_folder}/{str(id_flat)}.jpg', 'wb') as file:
                    file.write(img_bytes)

            id_flat += 1

        #задержка для парсинга одной страницы
        print(f'Обработалась страница {page}')
        time_stop = random.uniform(0, 5)
        time.sleep(time_stop)

    data = pd.DataFrame(home)
    data.to_csv('data_parsing.csv', sep=';', encoding='utf-8')

    if bool_table:
        print(data)

    print('Выполнение окончено')

parser(url = 'https://www.mr-group.ru/catalog/apartments/?project=45589&project_type=apartments&view_mode=list&building%5B%5D=all&floor%5B%5D=all&renovation%5B%5D=all&availability_renovation=all&sort=PROPERTY_IS_ENABLED_DESC&page=',
       page_start = 1, page_count = 2, bool_table = True, bool_pictures = False)
