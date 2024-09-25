#!/bin/bash
LMS=lms

# определение .env файла
export ENV_FILE=./.env

# Запуск миграций
docker-compose exec ${LMS} alembic upgrade head