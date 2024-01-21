import requests
from bs4 import BeautifulSoup
import os

url = f'https://www.kufar.by/l/mobilnye-telefony?ot=1&query=oneplus+nord+3&rgn=all&sort=lst.d&utm_filterOrigin=Search_suggester_3&utm_queryOrigin=Manually_typed&utm_suggestionType=Category_only'

request = requests.get(url)
soup = BeautifulSoup(request.text, 'html.parser')

all_item = soup.find_all("a", class_="styles_wrapper__5FoK7")
links = []
for link in all_item:
    links.append(link['href'])

photo_links = []
infini_dict = {}
for i in enumerate(links):
    new_request = requests.get(i[1])
    new_soup = BeautifulSoup(new_request.text, 'html.parser')
    h1_tag = new_soup.find('h1')
    items = new_soup.find_all("img", class_="styles_slide__image__vertical__QdnkQ")

    if items:
        infini_dict.clear()
        infini_dict[f'link{i[0]}'] = items[0]['src']
        infini_dict[f'title{i[0]}'] = h1_tag.text
        photo_links.append(infini_dict)
    else:
        print(f"Нет изображения по этой ссылке {i[1]}")

print(photo_links)

os.makedirs('downloaded_images', exist_ok=True)


