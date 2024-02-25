from jinja2 import Template


def to_html(contents, f_name, s_name, n_r_h):

    goal = s_name.replace(" ", "_").replace("/", "_").replace(":", "").replace("*", "_").replace("?", "_")
    cat = f_name.replace(" ", "_")

    not_error = ['Договорная', 'Бесплатно']

    sort_contents = sorted(contents, key=lambda x: float(x[2].replace(' ', '')[:-2]) if x[2] not in not_error else True, reverse=n_r_h)

    item = '''
    <!DOCTYPE HTML>
        <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>{{name}}</title>
                <meta name="description" content="Описание страницы" />
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
                <style>
                    html, body {
                        margin: 0;
                        padding: 0;
                        font-family: "Montserrat", sans-serif;
                        font-optical-sizing: auto;
                        font-style: normal;
                    }
                    
                    .card {
                        border: 1px solid grey;
                        border-radius: 5px;
                        flex-grow: 1;
                        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
                        background-color: lightgrey;
                    }
                    
                    .image {
                        width: 100%;
                    }
                    
                    .image img {
                        width: 100%;
                    }
                    
                    .text {
                        color: black;
                        padding-left: 10px;
                    }
                    
                    a {
                        font-size: 2em;
                        font-weight: 700;
                        text-decoration: none;
                        display:block;
                    }
                    .text a:hover {
                        font-weight: 900;
                        font-size: 1.95em;
                    }
                    
                </style>
            </head>
            <body>
                <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:30px;align-items:flex-start;">
                    {%- for x in sort_contents %}
                    {% if x[4] != False %}
                        <div class="card">
                            <div class="image">
                                <img src={{x[4]}}>
                            </div>
                            <div class="text">
                                <a href={{x[0]}}>{{x[1]}}</a>
                                <h2>{{x[2]}}</h2>
                                <p>{{x[3]}}</p>
                            </div>
                        </div>
                    {% else %}
                        <div class="card">
                            <div class="image">
                                <img src='https://turbok.by/public/img/no-photo--lg.png'>
                            </div>
                            <div class="text">
                                <a href={{x[0]}}>{{x[1]}}</a>
                                <h2>{{x[2]}}</h2>
                                <p>{{x[3]}}</p>
                            </div>
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

    print('HTML страница создана')
