В рамках проекта вам необходимо получить данные о компаниях и вакансиях с сайта hh.ru, 
спроектировать таблицы в БД PostgreSQL и загрузить полученные данные в созданные таблицы.

Создал конфигурационный файл database.ini. В котором хранится сама конфигурация. 
пример:
[postgresql]
host= 'Ваш локальный хост: ...'
user= 'Ваш локальный пользователь: ...'
password= 'Ваш локальный пароль: ...'
port= 'Ваш локальный порт: ...'

Добавил файл в .gitignore. Для безопасности.

Так как у себя использовал host=localhost, то есть свой локальный хост, а также имя юзера, пароль 
и порт, вам у себя нужно создать файл database.ini. Со своими настройками конфигурации.
