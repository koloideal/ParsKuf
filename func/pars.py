import time
from bs4 import BeautifulSoup
import requests
import os
import datetime
from func import helper, to_database, to_html


def pars(url, goal, cat):

    try:

        while True:

            try:

                need_to_reverse_html = int(input('\nКак сортировать результаты в HTML?(1 - От большего к меньшему, 0 - От меньшего к большему)\n'))

                if need_to_reverse_html in [0, 1]:

                    break

            except ValueError:

                print('Введено некорректное значение')

        print('\nВ процессе...\n')

        start_parsing = time.time()
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')

        all_item = soup.find_all("div", class_="styles_cards__bBppJ")

        about_item = []

        for i in all_item[0].contents:

            try:

                item = [i.a['href'], i.find('h3', class_="styles_title__F3uIe").text, i.find('p', class_='styles_price__G3lbO').text,
                        i.find('div', class_='styles_secondary__MzdEb').text, i.find('img', class_='styles_image__ZPJzx')['src']]

                about_item.append(item)

            except TypeError:

                item = [i.a['href'], i.find('h3', class_="styles_title__F3uIe").text, i.find('p', class_='styles_price__G3lbO').text,
                        i.find('div', class_='styles_secondary__MzdEb').text, False]

                about_item.append(item)

        cat = cat.replace(" ", "_")
        goal = goal.replace("+", "_")

        os.makedirs('utils', exist_ok=True)

        os.makedirs('content', exist_ok=True)

        os.makedirs(f'content/{cat}', exist_ok=True)

        os.makedirs(f'content/{cat}/{goal}', exist_ok=True)

        to_database.to_database(cat, goal, about_item)

        to_html.to_html(about_item, cat, goal, need_to_reverse_html)

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

            pass
    except IndexError:

        print('\nПо данному запросу ничего не найдено')

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

        yes_no = input('Желаете продолжить?(Y,N)\n').lower()

        if yes_no == 'y' or yes_no == 'yes':

            helper.helper()

        else:

            pass
