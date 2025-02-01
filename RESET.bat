@echo off
FOR %%s IN (company student teacher online_learning_platform) DO (
    DEL %%s\migrations\*.py
    TYPE nul > %%s\migrations\__init__.py
)
DEL db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
