#!/bin/bash

# определение .env файла
export ENV_FILE=./.env

# Остановка и удаление контейнеров
docker-compose -f docker-compose.local.yml down

# Запуск новых контейнеров 
docker-compose -f docker-compose.local.yml up -d --build

# удаление неиспользуемых образов
docker image prune -f
