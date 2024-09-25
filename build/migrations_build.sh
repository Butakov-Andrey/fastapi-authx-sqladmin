#!/bin/bash
LMS=lms

export ENV_FILE=./.env

echo -n "Введите сообщение для миграции: "
read migration_message

docker-compose exec ${LMS} alembic revision --autogenerate -m "$migration_message"