Для запуска проекта необходимо выполнить следующие шаги:

1. Установите Docker
Убедитесь, что Docker установлен на вашей машине. Если он еще не установлен, скачайте и установите его с официального сайта: https://www.docker.com/ .

2. Создайте .env файлы
Общий .env файл в корне проекта
Создайте файл .env в корне проекта (book-rental/) с базовыми настройками для всех микросервисов.

# Настройки PostgreSQL для user-service
USER_DB_USER=user
USER_DB_PASSWORD=password
USER_DB_NAME=db_name
USER_DB_HOST=user-db  # Имя сервиса базы данных из docker-compose.yml
USER_DB_PORT=5432

# Полный URL для подключения к PostgreSQL (используется в Alembic и FastAPI)
USER_DB_URL=postgresql+asyncpg://${USER_DB_USER}:${USER_DB_PASSWORD}@${USER_DB_HOST}:${USER_DB_PORT}/${USER_DB_NAME}

Примечание : Переменная USER_DB_URL используется для асинхронного подключения к базе данных через SQLAlchemy. Если вы хотите использовать её для Alembic, замените postgresql+asyncpg на postgresql. 

Локальный .env файл в папке user_service
Если вам нужен отдельный .env файл для user_service, создайте его в директории user_service/ с аналогичным содержимым.

3. Запустите контейнеры
После создания .env файлов выполните следующую команду для сборки и запуска всех контейнеров:
docker-compose up --build

4. Отладка при необходимости
Если возникнут проблемы, проверьте логи контейнеров:

docker-compose logs user-service
docker-compose logs user-db