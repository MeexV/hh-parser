import requests
import pprint
from pickle import dump, load
from os.path import exists
import re
from collections import Counter
from json import dump as jdump
from pycbrf import ExchangeRates
import statistics

def parser_vacancies(vacancy_name,vacancy_area, choise_pages = 1):
    DOMAIN = "https://api.hh.ru/"
    url_vacancies = f"{DOMAIN}vacancies"
    rate = ExchangeRates()    # курс валют

    if exists('area.pkl'):
        with open('area.pkl', mode='rb') as f:
            area = load(f)
    else:
        area = {}

    #vacancy_name = input("Введите название вакансии: ")
    #vacancy_area = input("Введите город: ")

    area_id = area.get(vacancy_area)
    if not area_id:
        response = requests.get(f"{DOMAIN}areas")
        areas = response.json()
        for area_info in areas:
            if area_info['name'] == vacancy_area:
                area_id = area_info['id']
                area[vacancy_area] = area_id
                with open('area.pkl', mode='wb') as f:
                    dump(area, f)
                break

    params = {
        "text": vacancy_name,
        "area": area_id
    }

    all_result = requests.get(url_vacancies, params=params).json()
    count_pages = all_result['pages']
    all_count_vacancies = len(all_result["items"])

    vacancy = {
        "Вакансия": vacancy_name,
        "Всего вакансий": all_count_vacancies,
        "Город": vacancy_area
    }
    salary = {
        'from': [],
        'to': []
    }
    skills_all = []

    #choise_pages = int(input("Введите количество страниц, которое хотите обработать: "))

    for page in range(count_pages):
        if page == choise_pages:
            break
        else:
            print(f"Обрабатывается страница {page}")

        params = {
            "text": vacancy_name,
            "page": page,
            "area": area_id
        }
        result = requests.get(url_vacancies, params=params).json()
        vacancy["Всего вакансий"] += len(all_result["items"])

        for res in result["items"]:
            skills = set()
            city = res["area"]["name"]
            # Добавление города в файл, если его нет
            if city not in area:
                area[city] = res['area']['id']

            res_full = requests.get(res['url']).json()
            # Описание вакансии
            vac_description = res_full['description']
            vac_description_en = re.findall(r"\s[A-Za-z-?]+", vac_description)    # Оставляем только английские слова
            set_description_skills = set(x.strip(' -').lower() for x in vac_description_en)
            for skill in res_full['key_skills']:
                skills_all.append(skill['name'].lower())
                skills.add(skill['name'].lower())

            for skill in set_description_skills:
                if not any(skill in x for x in skills):
                    skills_all.append(skill)
            # Обработка зарплаты
            if res_full['salary']:
                code = res_full['salary']['currency']
                if rate[code] is None:
                    code = 'RUR'
                k = 1 if code == 'RUR' else float(rate[code].value)
                salary['from'].append(1/k*res_full['salary']['from'] if res['salary']['from'] else 1/k*res_full['salary']['to'])
                salary['to'].append(1/k*res_full['salary']['to'] if res['salary']['to'] else 1/k*res_full['salary']['from'])
    count_skills = Counter(skills_all)
    avg_up = round(statistics.mean(salary['from']),2)
    avg_down = round(statistics.mean(salary['to']),2)
    vacancy.update({'Средняя зарплата от': avg_up,
                    'Средняя зарплата до': avg_down})
    list_sk = []

    for name, count in count_skills.most_common(5):
        list_sk.append({
            'Навыки': name,
            'Количество': count
        })
    total_count = sum([i['Количество'] for i in list_sk])
    for i in list_sk:
        i['Процент'] = round(i['Количество'] /total_count*100, 2)
    vacancy['Требования'] = list_sk
    pprint.pprint(vacancy)

    with open('result.json', mode='w', encoding='utf-8') as f:
        jdump([vacancy], f, ensure_ascii=False)
    with open('area.pkl', mode='wb') as f:
        dump(area, f)
    return vacancy
