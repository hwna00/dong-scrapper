from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from bs4 import BeautifulSoup

URL = 'https://www.kookmin.ac.kr/comm/menu/user/8b5cdb9e5a60a79bcf0abdd61e3f5732/content/index.do'


def get_dongs(url):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)

    search_results = browser.find_elements_by_class_name("cont_section")
    content = browser.page_source.encode('utf-8').strip()
    dongs = extract_dongs(content)
    toJson(dongs)

    browser.quit()

    return dongs


def extract_dongs(content):
    dongs = {}
    soup = BeautifulSoup(content, 'html.parser')
    page = soup.findAll('div', {'class', 'cont_section'})[1:]
    for section in page:
        title = section.find('p', {'class': 'cont_subtit'}).text
        item = section.find('tbody').findAll('tr')
        result = extract_dong(item)
        dongs[title] = result
        print(title + ' 정리 완료')
    return dongs


def extract_dong(dongs):
    payload = []
    for dong in dongs:
        items = dong.findAll('td')

        title = items[0].text
        location = items[3].text
        try:
            desc = items[2].text
        except UnboundLocalError:
            desc = '없음'

        payload.append({
            'title': title,
            'desc': desc,
            'location': location
        })
    return payload


def toJson(dict):
    with open('jung-dongs.json', 'w', encoding='utf-8') as file:
        json.dump(dict, file, ensure_ascii=False, indent='\t')


get_dongs(URL)
