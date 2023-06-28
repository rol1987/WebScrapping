import requests
import bs4
import lxml
from fake_headers import Headers
import json
import os
from pprint import pprint

def scrapp(link, word1, word2):
    headers = Headers(browser='firefox', os='win')
    headers_data = headers.generate()
    response = requests.get(link, headers=headers_data)
    html_data = response.text
    soup = bs4.BeautifulSoup(html_data, 'lxml')

    vacancy_card = soup.find_all('div', class_='serp-item') #Карточка вакансии
    vacancy_list = []

    for item in vacancy_card:
        dictionary = {'Название вакании': '', 'Ссылка': '', 'Вилка ЗП': '', 'Название компании': '', 'Город': ''}
        vacancy_name = item.find('a').text
        if vacancy_name.find(word1) != -1 or vacancy_name.find(word2) != -1:
            vacancy_company_name = item.find("a", class_="bloko-link bloko-link_kind-tertiary").text
            vacancy_link = item.find("a", class_="serp-item__title")["href"]
            vacancy_city = item.find('div', {"data-qa": True}, class_='bloko-text').text
            vacancy_money = item.find('div', class_='vacancy-serp-item-body__main-info').find('span', class_='bloko-header-section-3')

            # проверяем есть ли атрибут "text"
            if hasattr(vacancy_money, 'text'):
                vacancy_money = vacancy_money.text
            else:
                vacancy_money = 'none'

            dictionary['Название вакании'] = vacancy_name
            dictionary['Ссылка'] = vacancy_link
            dictionary['Вилка ЗП'] = vacancy_money
            dictionary['Название компании'] = vacancy_company_name
            dictionary['Город'] = vacancy_city
           
            vacancy_list.append(dictionary) # добавляем словарь в список
    
    json_object = json.dumps(vacancy_list, indent=4, ensure_ascii=False)

    # формируем путь к файлу json
    cwd = os.path.dirname(__file__)
    file_name = 'sample.json'
    full_path = os.path.join(cwd, file_name)
    
    # Записываем в json
    with open(full_path, "w",  encoding='utf-8') as outfile:
        outfile.write(json_object)

if __name__ == '__main__': 
    link_msk = 'https://hh.ru/search/vacancy?text=python&area=1&area=2'
    word1 = 'Python'
    word2 = 'Flask'
    scrapp(link_msk, word1, word2)