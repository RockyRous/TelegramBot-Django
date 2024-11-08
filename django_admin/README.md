Инициализация проекта Django:
```bash
django-admin startproject name .
```
Создание приложения:
```bash
python manage.py startapp name
```
Создание миграций:
```bash
docker-compose run django python manage.py makemigrations store
```
Применение миграций:
```bash
docker-compose run django python manage.py migrate
```
Создание суперпользователя:
```bash
docker-compose run django python manage.py createsuperuser
admin : admin
```
