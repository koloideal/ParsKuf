from func import pars


def helper():
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

    pars.pars(f'https://www.kufar.by/l/{link_categories.get(int(category))}/bez-posrednikov?query={target}&sort=lst.d', target, clear_cat)
