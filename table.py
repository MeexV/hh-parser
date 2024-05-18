import sqlite3
from sqlalchemy import Column, Integer, String, create_engine, REAL, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///hh2.sqlite', echo=True)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


requestpers_table = Table("vacanciesskills", Base.metadata,
                          Column('id', Integer, primary_key=True, autoincrement=True),
                          Column('VacancyID', Integer, ForeignKey('vacancies.VacancyID')),
                          Column('SkillID', Integer, ForeignKey('skills.SkillID')))


class Vacancies(Base):
    __tablename__ = 'vacancies'
    VacancyID = Column(Integer, primary_key=True, autoincrement=True)
    VacancyName = Column(String, nullable=True)
    VacancyArea = Column(String)
    TotalVacancies = Column(Integer, nullable=True)
    AvgSalaryFrom = Column(REAL, nullable=True, default=0)
    AvgSalaryTo = Column(REAL, nullable=True, default=0)

    def __init__(self, VacancyName, VacancyArea, TotalVacancies, AvgSalaryFrom, AvgSalaryTo):
        self.VacancyName = VacancyName
        self.VacancyArea = VacancyArea
        self.TotalVacancies = TotalVacancies
        self.AvgSalaryFrom = AvgSalaryFrom
        self.AvgSalaryTo = AvgSalaryTo


class Skills(Base):
    __tablename__ = 'skills'
    SkillID = Column(Integer, primary_key=True, autoincrement=True)
    SkillName = Column(String, nullable=True)

    def __init__(self, SkillName):
        self.SkillName = SkillName

class Requirements(Base):
    __tablename__ = 'requirements'
    RequirementID = Column(Integer, primary_key=True, autoincrement=True)
    VacancyID = Column(Integer, ForeignKey('vacancies.VacancyID'))
    SkillID = Column(Integer, ForeignKey('skills.SkillID'))
    Quantity = Column(Integer, nullable=True)
    Percentage = Column(REAL, nullable=True)


    def __init__(self, VacancyID, SkillID, Quantity, Percentage):
        self.VacancyID = VacancyID
        self.SkillID = SkillID
        self.Quantity = Quantity
        self.Percentage = Percentage


Base.metadata.create_all(engine)

def add_vacansies(result_pars):
    vacansies = Vacancies(result_pars['Вакансия'],
                          result_pars.get('Город', ''),
                          result_pars['Всего вакансий'],
                          result_pars['Средняя зарплата от'],
                          result_pars['Средняя зарплата до'])
    session.add(vacansies)
    session.commit()
    return vacansies.VacancyID

def add_skills(result_pars):
    skills = [x['Навыки'] for x in result_pars['Требования']]
    skill_ids = {}
    for skill in skills:
        skill_id = Skills(skill)
        session.add(skill_id)
        session.commit()
        skill_ids[skill] = skill_id.SkillID
    return skill_ids

def add_requirements(result_pars):
    requirements = [x for x in result_pars['Требования']]
    skill_ids = add_skills(result_pars)
    vacancy_id = add_vacansies(result_pars)
    for requirement in requirements:
        skill, quantity, percentage = requirement.values()
        session.add(Requirements(vacancy_id, skill_ids[skill], quantity, percentage))
        session.commit()



# conn = sqlite3.connect('hh.sqlite')
# cursor = conn.cursor()
#
# # Создание таблицы Vacancies
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Vacancies (
#     VacancyID INTEGER PRIMARY KEY AUTOINCREMENT,
#     VacancyName TEXT NOT NULL,
#     TotalVacancies INTEGER NOT NULL,
#     AvgSalaryFrom REAL NOT NULL,
#     AvgSalaryTo REAL NOT NULL
# )
# """)
#
# # Создание таблицы Skills
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Skills (
#     SkillID INTEGER PRIMARY KEY AUTOINCREMENT,
#     SkillName TEXT NOT NULL
# )
# """)
#
# # Создание таблицы Requirements
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Requirements (
#     RequirementID INTEGER PRIMARY KEY AUTOINCREMENT,
#     VacancyID INTEGER,
#     SkillID INTEGER,
#     Quantity INTEGER NOT NULL,
#     Percentage REAL NOT NULL,
#     FOREIGN KEY (VacancyID) REFERENCES Vacancies(VacancyID),
#     FOREIGN KEY (SkillID) REFERENCES Skills(SkillID)
# )
# """)


