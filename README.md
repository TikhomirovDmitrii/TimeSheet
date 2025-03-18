TimeSheet API

TimeSheet — это REST API на Django для учета рабочего времени.  
API позволяет управлять проектами, логами работы сотрудников,  
а также формировать отчеты по потраченным часам.

1) Запуск проекта

1. Клонируем репозиторий
```sh
git clone https://github.com/ТВОЙ_GITHUB_USERNAME/TimeSheet.git
cd TimeSheet

2. Устанавливаем зависимости
python -m venv .venv
source .venv/bin/activate  # (Linux/macOS)
.venv\Scripts\activate  # (Windows)

pip install -r requirements.txt

3. Настроим базу данных (PostgreSQL)
CREATE DATABASE timesheet_db;
CREATE USER timesheet_user WITH PASSWORD 'your_password';
ALTER ROLE timesheet_user SET client_encoding TO 'utf8';
ALTER ROLE timesheet_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE timesheet_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE timesheet_db TO timesheet_user;

python manage.py migrate

 4. Создадим суперпользователя
python manage.py createsuperuser

5. Запустим сервер
just up


2) Pre-commit хуки
Автоформатирование кода:
pre-commit run --all-files

Установка хуков:
pre-commit install
