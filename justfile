# Указываем, что команды будут выполняться через cmd
set shell := ["cmd", "/C"]

up:
    echo Запуск проекта...
    call .venv\Scripts\activate && python manage.py migrate && python manage.py runserver

# Установка зависимостей и настройка виртуального окружения
install:
    python -m venv .venv
    call .venv\Scripts\activate && pip install -r requirements.txt

# Применение миграций
migrate:
    call .venv\Scripts\activate && python manage.py migrate

# Создание суперпользователя
createsuperuser:
    call .venv\Scripts\activate && python manage.py createsuperuser

# Очистка базы данных и повторное применение миграций
reset-db:
    call .venv\Scripts\activate && python manage.py flush --no-input
    call .venv\Scripts\activate && python manage.py migrate

# Запуск сервера
runserver:
    call .venv\Scripts\activate && python manage.py runserver


# Удаление виртуального окружения
clean:
    rmdir /S /Q .venv

# Обновление зависимостей
update:
    call .venv\Scripts\activate && pip install --upgrade -r requirements.txt
