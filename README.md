# praktikum_new_diplom

### Ссылочки:
- http://localhost/api/docs/ - docks
- http://127.0.0.1:8000/swagger-ui/ - docs swagger
- http://localhost - foodgram front
- https://www.figma.com/file/HHEJ68zF1bCa7Dx8ZsGxFh/ - figma
- https://t.me/KorGolom  @KorGolom - telegram

### Админка:

admin_email=admin@admin.com

admin_login=admin

admin_password=admin228


### P.S. Ревьюеру

Денис, если ты всё ещё мой ревьюер, нервничаю из за того, что проект не полностью работает на Реакте, но одногруппники мне объяснили, что до конца проект допиливается уже после первых ревью и при деплое, а при работающем API можно уже отправлять на первое ревью. Поэтому отправляю в таком виде.


Да, апи работает. Через POSTMAN все запросы обрабаываются (надеюсь я ничего не пропустил). Создание и редактирование рецептов, подписки и отписки, избранные рецепты и т.д. Аутентификация через токен тоже работает.

### Запуск:

#### Виртуальное оркжуение

```
python -m venv venv
```

```
source venv/scripts/activate
```

#### Зависимости

```
pip install -r requirements.txt
```

```
python3 -m pip install --upgrade pip
```

#### Миграции (в папке backend/foodgram_backend/)

```
cd backend/foodgram_backen/
```

```
py manage.py makemigrations
```

```
py manage.py migrate
```

#### Сервер

```
py manage.py runserver
```

#### Фронт (в папке infra/)

```
cd infra/
```

```
docker-compose up
```
