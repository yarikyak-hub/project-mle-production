# Инструкции по запуску проекта

## Этап 1. Написание FastAPI-микросервиса

Для запуска микросервиса локально в виртуальном окружении выполните следующие команды:

Создайте виртуальное окружение:
```bash
python -m venv .venv
Активируйте его:

bash
.venv\Scripts\activate

Установите зависимости:

bash
pip install -r requirements.txt
Запустите сервер:

bash
uvicorn services.ml_service.main:app --host 127.0.0.1 --port 8000
Сервис будет доступен по адресу: http://127.0.0.1:8000. Документация Swagger: http://127.0.0.1:8000/docs.

Этап 2. Контейнеризация микросервиса
Для запуска микросервиса с помощью Docker выполните следующие шаги:

Соберите Docker-образ:

bash
docker build -f Dockerfile_ml_service -t ml_service:v1 .
Запустите контейнер с переменными окружения из файла services/.env:

bash
docker run -d --name my_ml_service -p 8000:8000 --env-file services/.env ml_service:v1
Сервис доступен по адресу: http://127.0.0.1:8000 (Swagger UI: /docs).

Этап 3. Запуск сервисов для системы мониторинга
Для запуска микросервиса и системы мониторинга (Prometheus и Grafana) в режиме Docker Compose выполните команду в корне проекта:

bash
docker compose up -d --build
Адреса сервисов после запуска:

Микросервис (FastAPI): http://127.0.0.1:8000 (Swagger UI: http://127.0.0.1:8000/docs)

Эндпоинт с метриками: http://127.0.0.1:8000/metrics

Prometheus: http://127.0.0.1:9090

Grafana: http://127.0.0.1:3000 (Логин: admin, Пароль: 1admin)

Этап 4. Построение дашборда для мониторинга
Для симуляции нагрузки на сервис выполните:

bash
python load_test.py

Дашборд Grafana сохранен в файле dashboard.json. 
Скриншот дашборда находится в файле dashboard.jpg.