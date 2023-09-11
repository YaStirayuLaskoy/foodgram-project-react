# praktikum_new_diplom

### Ссылочки:
- https://pohavat.ddns.net/ - домен

- http://localhost/api/docs/ - docks
- http://127.0.0.1:8000/swagger-ui/ - docs swagger
- http://localhost - foodgram front
- https://www.figma.com/file/HHEJ68zF1bCa7Dx8ZsGxFh/ - figma
- https://t.me/KorGolom  @KorGolom - telegram

### Админка:

admin_email=admin@admin.com

admin_login=admin

admin_password=admin228


### Запуск сервер:

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

### Запуск локально:

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


