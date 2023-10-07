# FoodGram

### Ссылка на FoodGram: https://foodgram.gq/recipes

## Описание
«Фудграм» — сайт, на котором пользователи публикуют рецепты, добавляют чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также доступен сервис «Список покупок». Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Целью проекта является практическое погружение в самостоятельное создания веб приложения, развертывание проекта на сервере с помощью контейнеров Docker.

![image_2023-10-04_01-12-05](https://github.com/YaStirayuLaskoy/foodgram-project-react/assets/122834885/3f9e6171-2d70-42a0-9452-91d5f6662f30)

### Немного подробнее про работу:
У веб-приложения был готовый фронтенд, написанное на фреймворке React. Файлы, необходимые для его сборки, хранятся в репозитории foodgram-project-react в папке frontend.

Кроме папки frontend в нём также были папки infra и docs:
- В папке infra — заготовка инфраструктуры проекта: конфигурационный файл nginx и docker-compose.yml.
- В папке docs — файлы спецификации API.

Моя задача как бэкенд-разработчика — написать бэкенд, включая API, для веб-приложения «Фудграм», а также опубликовать это веб-приложение на виртуальном удалённом сервере и сделать его доступным в интернете.<br>
Никаких жёстких рамок по структуре и содержанию кода не было, все решения по реализации были приняты самостоятельно. 

## Возможности проекта

- Регистрация и авторизация пользователей
- Добавление и изменение рецептов
- Просмотр рецептов других пользователей
- Добавление чужих рецептов в избранное
- Возможность подписываться на авторов рецептов
- Добавление ингредиентов рецепта в корзинку покупок и скачивание списка ингредиентов в формате txt


## Технологии и инструменты

- Python (Бэкенд)
- React (Фронтенд)
- База Данных [PostgreSQL](https://www.postgresql.org/)
- WSGI-сервер [Gunicorn](https://gunicorn.org/)
- WEB-сервер [Nginix](https://nginx.org/ru/docs/)
- Зарегистрированное доменное имя [No-ip](https://www.noip.com/)
- Шифрование через HTTPS [Let's Encrypt](https://letsencrypt.org/)
- Мониторинг доступности и сбор ошибок [UptimeRobot](https://uptimerobot.com/)
- Для обеспечения безопасности, секреты подгружаются из файла .env. В файле .env содержатся важные константы, которые строго исключены из хранения в коде проекта. Настройка находится в блоке "Как запустить Kittygram".
- [Docker](https://www.docker.com/products/docker-desktop/)
- Автоматизирровано тестирование и деплой проекта Kittygram с помощью GitHub Actions

## Ссылочки:
- https://pohavat.ddns.net/ - домен
- http://localhost/api/docs/ - docks
- http://127.0.0.1:8000/swagger-ui/ - docs swagger
- http://localhost - front local (запуск через контейнер)
- https://www.figma.com/file/HHEJ68zF1bCa7Dx8ZsGxFh/ - figma (запуск через контейнер)
- https://t.me/KorGolom  @KorGolom - telegram

## Запуск сервер:

```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin 
```

#### Перенести *docker-compose.production.yml* на сервер

```
scp -i path_to_SSH/SSH_name docker-compose.yml \
    username@server_ip:/home/username/foodgram/docker-compose.production.yml
```
#### Перенести *.env* на сервер, вставив туда значения из .env.template

```
scp -i path_to_SSH/SSH_name .env \
    username@server_ip:/home/foodgram/.env
```

- path_to_SSH — путь к файлу с SSH-ключом;
- SSH_name — имя файла с SSH-ключом (без расширения);
- username — ваше имя пользователя на сервере;
- server_ip — IP вашего сервера.


#### Запустить демона

```
sudo docker compose -f docker-compose.production.yml up -d
```

#### Выполнить миграции

```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/static/. /static/
```

## Запуск локально:

#### Виртуальное окружение

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


