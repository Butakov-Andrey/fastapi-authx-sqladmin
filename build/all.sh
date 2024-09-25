#!/bin/bash

# определение .env файла
export ENV_FILE=./.env

# Остановка и удаление контейнеров
docker-compose -f docker-compose.yml down

# Запуск новых контейнеров 
docker-compose -f docker-compose.yml up -d --build

# удаление неиспользуемых образов
docker image prune -f
