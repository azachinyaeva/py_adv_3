import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json


headers_gen = Headers(os='win', browser='chrome')

vacancies_page = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2',
                              headers=headers_gen.generate())

vacancies_page_html = vacancies_page.text
vacancies_soup = BeautifulSoup(vacancies_page_html, 'lxml')
vacancies = vacancies_soup.find('main', class_='vacancy-serp-content')
vacancy_tags = vacancies.find_all('div', class_='vacancy-serp-item-body')

vacancy_result = [{}]

for vacancy_tag in vacancy_tags:
    header_tag = vacancy_tag.find('h3')
    a_tag = header_tag.find('a', class_='serp-item__title')
    vacancy_link = a_tag.get('href')
    job_title = a_tag.text
    salary_tag = vacancy_tag.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation', 'class': 'bloko-header-section-2'})
    if salary_tag:
        salary = salary_tag.text
    else:
        salary = "Не указана"
    company_tag = vacancy_tag.find('a', {'data-qa': 'vacancy-serp__vacancy-employer',
                                         'class': 'bloko-link bloko-link_kind-tertiary'})
    company = company_tag.text
    city_tag = vacancy_tag.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
    city = city_tag.text

    vacancy_result.append({
        'link': vacancy_link,
        'salary': salary.replace('\u202f', ''),
        'company': company.replace('\xa0', ' '),
        'job_title': job_title,
        'city': city.replace('\xa0', ' ')})

with open('vacancy.json', 'w', encoding='utf-8') as f:
    json.dump(vacancy_result, f, ensure_ascii=False, indent=4)
