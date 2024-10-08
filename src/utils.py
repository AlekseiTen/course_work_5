import os
from configparser import ConfigParser
import psycopg2
from config import ROOT_DIR

path = os.path.join(ROOT_DIR, 'database.ini')


def connect(filename="database.ini"):
    '''коннектор для соединения с БД. при вызове можно передать другие аргументы '''
    config = ConfigParser()
    config.read(filename)
    database_config = dict(config.items('database'))
    conn = psycopg2.connect(
        host=database_config['host'],
        database=database_config['database'],
        user=database_config['user'],
        password=database_config['password'],
        port=database_config['port'],
    )
    return conn


def create_tables(conn):
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях."""

    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                    employer_id INT PRIMARY KEY,
                    employer_name VARCHAR(100) NOT NULL
                )
            """)

            cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INT REFERENCES employers(employer_id),
                    vacancy_name VARCHAR(100) NOT NULL,
                    salary INT NOT NULL,
                    currency VARCHAR(100),
                    requirement TEXT,
                    vacancy_url VARCHAR(100) NOT NULL
                )
            """)


def loads_into_table(conn, vacansies: list) -> None:
    '''заполняет таблицу данными о вакансиях'''

    with conn:
        with conn.cursor() as cur:
            for vac in vacansies:
                cur.execute('INSERT INTO employers (employer_id, employer_name) VALUES '
                            '(%s,%s)' 'ON CONFLICT (employer_id) DO NOTHING', (vac.employer_id, vac.employer_name))

                cur.execute(
                    'INSERT INTO vacancies (vacancy_id, employer_id, vacancy_name, salary, currency, '
                    'requirement, vacancy_url) VALUES '
                    '(%s,%s,%s,%s,%s,%s, %s)',
                    (vac.vacancy_id, vac.employer_id, vac.vacancy_name, vac.salary, vac.currency,
                     vac.requirement, vac.vacancy_url))


def drop_table(conn, table_name) -> None:
    '''удаляет таблицу. по умолчанию соединение закроется. если передать в con_status 1 то останется открытым'''

    with conn:
        with conn.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f'из базы данных удалена таблица {table_name}')


# if __name__ == '__main__':
#     vacancies = [
#         Vacancy(1, "Developer", "http://example.com/job1", 60000,
#                 "RUR", "Разработчик", '1', 'Яндекс'),
#         Vacancy(2, "Designer", "http://example.com/job2", 70000,
#                 "USD", "Дизайнер", '1', 'Яндекс'),
#         Vacancy(3, "Blogger", "http://example.com/job3", 50000,
#                 "EURO", "Блоггер", '2', 'Ютьюб'),
#         Vacancy(4, "Web", "http://example.com/job4", 80000,
#                 "RUR", "Верстальщик", '3', 'ООО Верстка')
#     ]
#
#     conn_path = connect(path)
#     create_tables(conn_path)
#     loads_into_table(conn_path, vacancies)
#     drop_table(conn_path,'employers')