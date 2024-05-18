from flask import Flask, render_template, request
from parser import parser_vacancies
import sqlite3
from table import add_vacansies, add_skills, add_requirements

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contacts/')
def contacts():
    context = {'email': 'HHParser@gmail.ru',
               'number': '+7 (654) 651-51-88',
               'adres': 'г. Москва, 2-й Кожевнический переулок, 11'}
    return render_template('contacts.html', **context)


@app.route('/form/')
def vacancies():
    return render_template('vacancies.html')


@app.route('/result/', methods=['POST'])
def result():
    vacancy_area = request.form["vacancy_area"]
    vacancy_name = request.form['vacancy_name']
    result_pars = parser_vacancies(vacancy_name, vacancy_area)
    add_vacansies(result_pars)
    add_skills(result_pars)
    add_requirements(result_pars)




    # conn = sqlite3.connect('hh.sqlite')
    # cursor = conn.cursor()
    #
    # # Таблица Vacancies
    # cursor.execute("""
    # INSERT INTO Vacancies (VacancyName, TotalVacancies, AvgSalaryFrom, AvgSalaryTo)
    # VALUES (?, ?, ?, ?)
    # """, (result_pars['Вакансия'], result_pars['Всего вакансий'], result_pars['Средняя зарплата от'],
    #       result_pars['Средняя зарплата до']))
    #
    # # Таблица Skills
    # vacancy_id = cursor.lastrowid
    # skills = [x['Навыки'] for x in result_pars['Требования']]
    # skill_ids = {}
    # for skill in skills:
    #     cursor.execute("""
    #     INSERT INTO Skills (SkillName) VALUES (?)
    #     """, (skill,))
    #     skill_ids[skill] = cursor.lastrowid
    #
    # # Таблица Requirements
    # requirements = [x for x in result_pars['Требования']]
    # for requirement in requirements:
    #     skill, quantity, percentage = requirement.values()
    #     cursor.execute("""
    #     INSERT INTO Requirements (VacancyID, SkillID, Quantity, Percentage)
    #     VALUES (?, ?, ?, ?)
    #     """, (vacancy_id, skill_ids[skill], quantity, percentage))
    # conn.commit()
    # cursor.close()
    # conn.close()

    return render_template('result.html', result_pars=result_pars)


if __name__ == '__main__':
    app.run(debug=True)
