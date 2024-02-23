import time
from bs4 import BeautifulSoup
import requests
import os
import datetime
from func import helper


def pars(url, goal, cat):

    start_parsing = time.time()
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')

    all_item = soup.find_all("div", class_="styles_cards__bBppJ")

    about_item = []

    for i in all_item[0].contents:

        try:

            item = [i.a['href'], i.find('h3', class_="styles_title__F3uIe").text, i.find('p', class_='styles_price__G3lbO').text,
                    i.find('div', class_='styles_secondary__MzdEb').text, i.img['src']]

            about_item.append(item)

        except TypeError:

            item = [i.a['href'], i.find('h3', class_="styles_title__F3uIe").text, i.find('p', class_='styles_price__G3lbO').text,
                    i.find('div', class_='styles_secondary__MzdEb').text, False]

            about_item.append(item)

    try:
        cat = cat.replace(" ", "_").replace("/", "_").replace(":", "").replace("*", "_")
        goal = goal.replace("+", "_")

        os.makedirs('content', exist_ok=True)

        os.makedirs(f'content/{cat}', exist_ok=True)

        os.makedirs(f'content/{cat}/{goal}', exist_ok=True)

        for item in about_item:

            alt = item[1].replace(" ", "_").replace("/", "").replace(":", "").replace("*", "_") + '(' + item[0][30:34] + ')'

            try:

                os.makedirs(f'content/{cat}/{goal}/{alt}')

            except FileExistsError:

                continue

            else:

                if item[4]:

                    photo = requests.get(item[4])

                    with open(f'content/{cat}/{goal}/{alt}/{alt}.jpg', 'wb') as out:
                        out.write(photo.content)

                with open(f'content/{cat}/{goal}/{alt}/about.txt', 'w', encoding='utf8') as about:
                    about.write(f'Ссылка на товар : {item[0]}\n\n')
                    about.write(f'Цена : {item[2]}\n\n')
                    about.write(f'Локация товара : {item[3]}\n\n')

        print('\nУспешно завершено.')

        end_parsing = time.time()

        with open('utils/stats.txt', 'a', encoding='utf8') as logs:
            logs.write(f'Поиск вёлся по ключевой фразе - {goal}\n')
            logs.write(f'Найдено объявлений - {len(about_item)}\n')
            logs.write(f'Дата поиска - {datetime.datetime.now()}\n')
            logs.write(f'Категория поиска - {cat}\n')
            logs.write(f'Время поиска - {round(end_parsing - start_parsing, 4 )}\n\n')

        print(f'\nВремя поиска {round(end_parsing - start_parsing, 4)} с. ')
        print(f'Найдено объявлений - {len(about_item)}')
        print(f'Результаты парсинга сохранены в content/{cat}/{goal}/\n')

        yes_no = input('Желаете продолжить?(Y,N)\n')

        if yes_no == 'Y':

            helper.helper()

        else:

            print('\nУдачи !\n')

    except Exception as e:

        with open('utils/errors.txt', 'a', encoding='utf8') as g:
            g.write(f'Ошибка - {e}\n'
                    f'Дата - {datetime.datetime.now()}\n\n')

        print('\nЗавершено с ошибкой.')

        end_parsing = time.time()

        with open('utils/stats.txt', 'a', encoding='utf8') as logs:
            logs.write(f'Поиск вёлся по ключевой фразе - {goal}\n')
            logs.write(f'Найдено объявлений - {len(about_item)}\n')
            logs.write(f'Дата поиска - {datetime.datetime.now()}\n')
            logs.write(f'Категория поиска - {cat}\n')
            logs.write(f'Время поиска - {round(end_parsing - start_parsing, 4)}\n\n')

        print(f'\nВремя поиска {round(end_parsing - start_parsing, 4)} с.\n ')
        print(f'Найдено объявлений - {len(about_item)}')
        print(f'Результаты парсинга сохранены в content/{cat}/{goal}/\n')

        yes_no = input('Желаете продолжить?(Y,N)\n')

        if yes_no == 'Y':

            helper.helper()

        else:

            print('\nУдачи !\n')
