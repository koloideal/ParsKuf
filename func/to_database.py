import sqlite3


def to_database(f_name, s_name, contents):

    goal = s_name.replace(" ", "_").replace("/", "_").replace(":", "").replace("*", "_").replace("?", "_")
    cat = f_name.replace(" ", "_")

    connection = sqlite3.connect(f'content/{cat}/{goal}/{goal}.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS content (
    link TEXT,
    alt TEXT,
    price REAL,
    about TEXT,
    src TEXT
    )
    ''')

    connection.commit()

    cursor.execute('SELECT link FROM content')
    links = cursor.fetchall()

    res_links = []

    for i in links:

        for j in i:

            res_links.append(j[:35])

    for item in contents:

        if item[0][:35] not in res_links:

            alt = item[1].replace(" ", "_").replace("/", "").replace(":", "").replace("*", "_") + '(' + item[0][30:34] + ')'
            price = item[2].replace(' ', '')

            try:

                price = float(price[:-2])

            except ValueError:

                price = 0.0

            cursor.execute('INSERT INTO content(link, alt, price, about, src) VALUES ("%s","%s","%s","%s","%s")' % (item[0], alt, price, item[3], item[4]))
            connection.commit()

        else:

            continue

    connection.commit()
    cursor.close()

    print('База данных успешно создана\n')
