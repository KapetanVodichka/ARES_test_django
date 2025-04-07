# ARES Test Django Project

Этот проект представляет собой веб-приложение, созданное на фреймворке Django, которое выполняет парсинг данных, получаемых по API.  
Присутствуют сортировка, пагинация и фильтрация.

Ссылка на ТЗ: https://docs.google.com/document/d/1y5aPhk8Na8Hl1eVJKx1GJaZ5p3U25G9vdn87925mV2Q/edit?tab=t.0

## Требования
- **Python**: Версия 3.10 или выше. (При разработке использовался 3.11)

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/KapetanVodichka/ares_test_django.git
cd ares_test_django
```

### 2. Создание и активация виртуального окружения
```bash
python -m venv venv
```
```bash
venv\Scripts\activate  # Для Windows
# или
source venv/bin/activate  # Для Linux/Mac
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Применение миграций
В качесте БД используется sqlite, поэтому создавать и настраивать его не нужно. Остается только применить миграции для инициализации БД.
```bash
python manage.py migrate
```

### 5. Запуск приложения
```bash
python manage.py runserver
```

Парсер будет доступен по адресу http://127.0.0.1:8000.
