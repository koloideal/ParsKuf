import requests
from bs4 import BeautifulSoup
import os
import datetime
import time


def time_is(func):

    def wrap(j, k, c):

        start = time.time()

        value = func(j, k, c)

        end = time.time()

        result = end - start

        print(f'Функция выполнилась за {round(result, 4)} с.')

        return value

    return wrap


@time_is
def pars(url, goal, cat):

    start_parsing = time.time()
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

    for c, j in enumerate(location):

        about_item[c].append(j.text)

    photo_links = []

    try:

        for img in photo_item:

            item = [img.get('src'), img.get('alt')]
            photo_links.append(item)

        os.makedirs('content', exist_ok=True)

        os.makedirs(f'content/{cat.replace(" ", "_")}', exist_ok=True)

        os.makedirs(f'content/{cat.replace(" ", "_")}/{goal.replace("+", "_")}', exist_ok=True)

        for k, photo_link in enumerate(photo_links):

            alt = photo_link[1].replace(" ", "_").replace("/", "").replace(":", "")
            idx = 0

            try:

                os.makedirs(f'content/{cat.replace(" ", "_")}/{goal.replace("+", " ")}/{alt}')

            except FileExistsError:

                with open(f'content/{cat.replace(" ", "_")}/{goal.replace("+", " ")}/{alt}/about.txt', 'r', encoding='utf8') as e:
                    line = e.readline()

                if line[18:53] == about_item[k][0][:35]:

                    continue

                else:

                    try:

                        idx += 1

                        alt = photo_link[1].replace(" ", "_").replace("/", "") + '(' + str(idx) + ')'
                        os.makedirs(f'content/{cat.replace(" ", "_")}/{goal.replace("+", " ")}/{alt}')

                        photo = requests.get(photo_link[0])

                        with open(f'content/{cat.replace(" ", "_")}/{goal.replace("+", " ")}/{alt}/{alt}.jpg', 'wb') as out:
                            out.write(photo.content)

                        with open(f'content/{cat.replace(" ", "_")}/{goal.replace("+", " ")}/{alt}/about.txt', 'w', encoding='utf8') as about:
                            about.write(f'Ссылка на товар : {about_item[k][0]}\n\n')
                            about.write(f'Цена : {about_item[k][1]}\n\n')
                            about.write(f'Локация товара : {about_item[k][2]}\n\n')

                    except IndexError:

                        with open(f'content/{cat.replace(" ", "_")}/{goal.replace("+", " ")}/{alt}/about.txt', 'w', encoding='utf8') as about:
                            about.write(f'Ссылка на товар : {about_item[k][0]}\n\n')
                            about.write('Цена : неизвестно\n')
                            about.write(f'Цена : {about_item[k][1]}\n\n')

                    except FileExistsError as error:

                        with open('errors.txt', 'a', encoding='utf8') as errors:

                            errors.write(f'Ошибка - {error}\n'
                                         f'Дата - {datetime.datetime.now()}\n\n')

                        print('В текущей версии скрипта не поддерживается более 2-ух товаров с одинаковым названием, '
                              'последний товар с одинаковым названием будет проигнорирован.')

                        continue

            else:

                photo = requests.get(photo_link[0])

                with open(f'content/{cat.replace(" ", "_")}/{goal.replace("+", " ")}/{alt}/{alt}.jpg', 'wb') as out:
                    out.write(photo.content)

                try:

                    with open(f'content/{cat.replace(" ", "_")}/{goal.replace("+", " ")}/{alt}/about.txt', 'w', encoding='utf8') as about:
                        about.write(f'Ссылка на товар : {about_item[k][0]}\n\n')
                        about.write(f'Цена : {about_item[k][1]}\n\n')
                        about.write(f'Локация товара : {about_item[k][2]}\n\n')

                except IndexError:

                    with open(f'content/{cat.replace(" ", "_")}/{goal.replace("+", " ")}/{alt}/about.txt', 'w', encoding='utf8') as about:
                        about.write(f'Ссылка на товар : {about_item[k][0]}\n\n')
                        about.write('Цена : неизвестно\n\n')
                        about.write(f'Локация товара : {about_item[k][1]}\n\n')

        print('Завершено.')

        end_parsing = time.time()

        with open('stats.txt', 'a', encoding='utf8') as logs:
            logs.write(f'Поиск вёлся по ключевой фразе - {goal.replace("+", " ")}\n')
            logs.write(f'Найдено объявлений - {len(photo_links)}\n')
            logs.write(f'Дата поиска - {datetime.datetime.now()}\n')
            logs.write(f'Категория поиска - {cat}\n')
            logs.write(f'Время поиска - {round(end_parsing - start_parsing, 4 )}\n\n')

    except Exception as e:

        with open('errors.txt', 'a', encoding='utf8') as g:
            g.write(f'Ошибка - {e}\n'
                    f'Дата - {datetime.datetime.now()}\n\n')

        print('Завершено с ошибкой.')

        end_parsing = time.time()

        with open('stats.txt', 'a', encoding='utf8') as logs:
            logs.write(f'Поиск вёлся по ключевой фразе - {goal.replace("+", " ")}\n')
            logs.write(f'Найдено объявлений - {len(photo_links)}\n')
            logs.write(f'Дата поиска - {datetime.datetime.now()}\n')
            logs.write(f'Категория поиска - {cat}\n')
            logs.write(f'Время поиска - {round(end_parsing - start_parsing, 4)}\n\n')


all_categories = {

    1: '1 - Мобильные телефоны',
    2: '2 - Зарядные устройства для смартфонов',
    3: '3 - Чехлы для смартфонов',
    4: '4 - Портативные зарядные устройства',
    5: '5 - Планшеты',
    6: '6 - Умные часы и фитнес-браслеты',
    7: '7 - Наушники',
    8: '8 - Ноутбуки',
    9: '9 - Компьютеры',
    10: '10 - Мониторы',
    11: '11 - Комплектующие для ПК',
    12: '12 - Периферия и аксессуары'

}

link_categories = {

    1: 'mobilnye-telefony',
    2: 'zaryadnye-ustrojstva',
    3: 'chehly-kejsy',
    4: 'power-bank',
    5: 'planshety',
    6: 'umnye-chasy-i-fitnes-braslety',
    7: 'naushniki',
    8: 'noutbuki',
    9: 'sistemnye-bloki',
    10: 'monitory',
    11: 'komplektuyushchie-dlja-kompjutera',
    12: 'kompjuternaja-periferiya-i-aksessuary'

}

for i in all_categories.values():
    print(i)

while True:

    try:

        category = input('\nВведите номер категории интересующего вас товара: ').strip(' .')

        clear_cat = all_categories.get(int(category))[4:].strip()

        break

    except (TypeError, ValueError):

        print('Неправильно введённый номер, повторите ')

print(f'\nОбъявления будут искаться в категории "{clear_cat}"')

target = input('\nВведите название интересующего вас устройства: \n').replace(' ', '+')
print('В процессе...')

pars(f'https://www.kufar.by/l/{link_categories.get(int(category))}/bez-posrednikov?query={target}&sort=lst.d', target, clear_cat)

