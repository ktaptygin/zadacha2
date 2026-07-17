# zadacha2
# Hungry People — сайт ресторана

Адаптивное веб-приложение ресторана, разработанное на Python и Django в рамках технологической практики.

Проект создан на основе макета Figma. В приложении реализованы динамический вывод содержимого, регистрация и авторизация пользователей, бронирование столиков, контактная форма, отправка писем, восстановление пароля и административная панель.

# Основные возможности

- адаптивная вёрстка для компьютеров, планшетов и телефонов;
- мобильное меню;
- фиксированная навигационная панель;
- регистрация, вход и выход без перезагрузки страницы;
- хранение пользовательской сессии;
- восстановление пароля по электронной почте;
- бронирование столика через AJAX;
- отправка информации о бронировании на электронную почту;
- контактная форма;
- динамическое меню ресторана;
- фильтрация блюд по категориям;
- вывод не более 21 позиции на главной странице;
- слайдер специальных предложений;
- динамические разделы About Us, Our Team и Private Events;
- интеграция Яндекс Карты;
- административная панель Django;
- автоматические тесты.

# Используемые технологии

- Python;
- Django 4.2;
- SQLite;
- HTML5;
- CSS3;
- JavaScript;
- jQuery;
- AJAX;
- Bootstrap;
- Slick Carousel;
- методология БЭМ;
- Git и GitHub.

# Структура проекта

```text
zadacha2/
├── core/
│   ├── settings.py           # Настройки Django
│   ├── urls.py               # Маршруты проекта
│   ├── asgi.py
│   └── wsgi.py
├── restaurant/
│   ├── fixtures/             # Начальные данные в формате JSON
│   ├── migrations/           # Миграции базы данных
│   ├── static/restaurant/    # CSS, JavaScript и изображения
│   ├── templates/restaurant/ # HTML-шаблоны
│   ├── admin.py              # Настройка административной панели
│   ├── models.py             # Модели базы данных
│   ├── tests.py              # Автоматические тесты
│   └── views.py              # Серверная логика
├── manage.py
├── requirements.txt
└── README.md
```

# Маршруты приложения

| Метод | Маршрут | Назначение |
|---|---|---|
| GET | `/` | Главная страница |
| POST | `/booking/create/` | Создание бронирования |
| POST | `/contact/create/` | Отправка контактной формы |
| POST | `/auth/login/` | Авторизация пользователя |
| POST | `/auth/register/` | Регистрация пользователя |
| POST | `/auth/logout/` | Выход из системы |
| POST | `/auth/password-reset/` | Запрос восстановления пароля |
| GET/POST | `/auth/password-reset/<uid>/<token>/` | Установка нового пароля |
| GET | `/admin/` | Административная панель |

# Модели базы данных

| Модель | Назначение |
|---|---|
| `Booking` | Бронирования столиков |
| `Contact` | Сообщения контактной формы |
| `DeliciousCategory` | Категории меню |
| `Delicious` | Позиции меню |
| `Event` | Частные мероприятия |
| `Speciality` | Специальные предложения |
| `StaticSection` | Содержимое разделов сайта |
| `UserProfile` | Дополнительные данные пользователя |

# Установка и запуск

# 1. Клонирование проекта

```bash
git clone https://github.com/ktaptygin/zadacha2.git
cd zadacha2
```

# 2. Создание виртуального окружения

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Для Windows:

```bash
.venv\Scripts\activate
```

# 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

# 4. Создание базы данных

```bash
python manage.py migrate
```

# 5. Загрузка начальных данных

```bash
python manage.py loaddata restaurant/fixtures/page_content.json
python manage.py loaddata restaurant/fixtures/specialities.json
```

# 6. Создание администратора

```bash
python manage.py createsuperuser
```

# 7. Запуск сервера

```bash
python manage.py runserver
```

После запуска сайт доступен по адресу:

```text
http://127.0.0.1:8000/
```

Административная панель:

```text
http://127.0.0.1:8000/admin/
```

# Настройка электронной почты

Для отправки писем через Gmail перед запуском сервера необходимо установить переменные окружения:

```bash
export EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
export EMAIL_HOST='smtp.gmail.com'
export EMAIL_PORT='587'
export EMAIL_USE_TLS='true'
export EMAIL_HOST_USER='your_email@gmail.com'
export EMAIL_HOST_PASSWORD='your_application_password'
export DEFAULT_FROM_EMAIL='your_email@gmail.com'
export RESTAURANT_EMAIL='recipient@gmail.com'
```

В `EMAIL_HOST_PASSWORD` используется пароль приложения Google, а не обычный пароль от аккаунта.

Настоящие пароли и другие секретные данные нельзя добавлять в README или отправлять в GitHub.

# Тестирование

Для запуска автоматических тестов используется команда:

```bash
python manage.py test
```

Успешный результат:

```text
Ran 5 tests

OK
```

# Наполнение сайта

Начальные данные хранятся в JSON-фикстурах:

```text
restaurant/fixtures/page_content.json
restaurant/fixtures/specialities.json
```

После загрузки фикстур в базе появляются разделы сайта, категории, позиции меню, специальные предложения и мероприятия.
