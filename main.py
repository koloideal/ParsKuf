import requests
from bs4 import BeautifulSoup
import os
import datetime

url = 'https://www.kufar.by/l/mobilnye-telefony/bez-posrednikov?ot=1&query=OnePlus+10+Pro&sort=lst.d'
request = requests.get(url)
soup = BeautifulSoup(request.text, 'html.parser')

all_item = soup.find_all("a", class_="styles_wrapper__5FoK7")
photo_item = soup.find_all('img', class_="styles_image__ZPJzx")
prices = soup.find_all('p', class_='styles_price__G3lbO')
location = soup.find_all('div', class_='styles_secondary__MzdEb')

about_item = []
for link in all_item:

    about_item.append([link['href']])

for k, i in enumerate(prices):

    about_item[k].append(i.text)

for k, i in enumerate(location):

    about_item[k].append(i.text)


photo_links = []

for img in photo_item:

    item = [img.get('src'), img.get('alt')]
    photo_links.append(item)

os.makedirs('content', exist_ok=True)    


for k, photo_link in enumerate(photo_links):

    alt = photo_link[1].replace(" ", "_").replace("/", "")
    idx = 0

    try:

        os.makedirs(f'content/{alt}')

    except FileExistsError:

        with open(f'content/{alt}/about.txt', 'r', encoding='utf8') as e:
            line = e.readline()

        if line[18:53] == about_item[k][0][:35]:

            continue

        else:

            try:

                idx += 1

                alt = photo_link[1].replace(" ", "_").replace("/", "") + '(' + str(idx) + ')'
                os.makedirs(f'content/{alt}')

                photo = requests.get(photo_link[0])

                with open(f'content/{alt}/{alt}.jpg', 'wb') as out:
                    out.write(photo.content)

                with open(f'content/{alt}/about.txt', 'w', encoding='utf8') as about:
                    about.write(f'Ссылка на товар : {about_item[k][0]}\n\n')
                    about.write(f'Цена : {about_item[k][1]}\n\n')
                    about.write(f'Локация товара : {about_item[k][2]}\n\n')

            except FileExistsError as error:

                with open('errors.txt', 'a', encoding='utf8') as errors:

                    errors.write(f'Ошибка - {error}\n'
                                 f'Дата - {datetime.datetime.now()}\n\n')

                print('В текущей версии скрипта не поддерживается более 2-ух товаров с одинаковым названием,'
                      'последний товар с одинаковым названием будет проигнорирован.')

                continue

    else:

        photo = requests.get(photo_link[0])

        with open(f'content/{alt}/{alt}.jpg', 'wb') as out:
            out.write(photo.content)

        with open(f'content/{alt}/about.txt', 'w', encoding='utf8') as about:
            about.write(f'Ссылка на товар : {about_item[k][0]}\n\n')
            about.write(f'Цена : {about_item[k][1]}\n\n')
            about.write(f'Локация товара : {about_item[k][2]}\n\n')


print("Complete.")
