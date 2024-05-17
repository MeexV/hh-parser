from flask import Flask, render_template, request
from parser import parser_vacancies

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
    # print(result_pars)
    return render_template('result.html', result_pars=result_pars)


if __name__ == '__main__':
    app.run(debug=True)
