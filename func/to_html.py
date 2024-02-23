from jinja2 import Template


def to_html(contents, f_name, s_name):

    goal = s_name.replace(" ", "_").replace("/", "_").replace(":", "").replace("*", "_")
    cat = f_name.replace(" ", "_")

    sort_contents = sorted(contents, key=lambda x: float(x[2].replace(' ', '')[:-2]) if x[2] != 'Договорная' else True)

    item = '''
    <!DOCTYPE HTML>
    
        <style>
            p{
                font-size:large;
                font-family: sans-serif;
                font-weight: bold;
                background-color: #E35D36;
                border-radius: 20px;
                padding: 10px;
                text-align: center;
            }
            a{
                font-size:large;
                font-family: Roboto, sans-serif;
                font-weight: bold;
                text-decoration: None;
                background-color: #427777;
                border-radius: 20px;
                padding: 10px;
                text-align: center;
                color: #E3AF36;
            }
            a:hover{
                color: #a82828;
                background-color: #E39A36;
            }
            div{
                background-color: #e3a982;
                border-bottom-left-radius: 20px;
                border-bottom-right-radius: 20px;
                border-top-right-radius: 20px;
                padding: 10px;
                display: flex;
                flex-direction: column;
                width: 350px;
                margin-bottom: 50px;
            }
            
        </style>
        <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>{{name}}</title>
                <meta name="description" content="Описание страницы" />
            </head>
            <body>
                {%- for x in sort_contents %}
                {% if x[4] != False %}
                    <img src={{x[4]}}>
                    <div>
                        <a href={{x[0]}}>Ссылка на товар</a>
                        <p>{{x[1]}}</p>
                        <p>{{x[2]}}</p>
                        <p>{{x[3]}}</p>
                    </div>
                {% else %}
                    <img src='https://turbok.by/public/img/no-photo--lg.png' width='370' height='280'>
                    <div>
                        <a href={{x[0]}}>Ссылка на товар</a>
                        <p>{{x[1]}}</p>
                        <p>{{x[2]}}</p>
                        <p>{{x[3]}}</p>
                    </div>
                {% endif %}
                {% endfor -%}
                </div>
            </body>
        </html>\n\n'''

    obj = Template(item)
    message = obj.render(name=s_name, sort_contents=sort_contents)

    with open(f'content/{cat}/{goal}/{goal}.html', 'w', encoding='utf8') as result:
        result.write(message)

    print('HTML страница создана\n')
