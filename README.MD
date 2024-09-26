# LMS ALPHA

## TODO
- https://github.com/yezz123/AuthX
- https://aminalaee.dev/sqladmin/authentication/

## Начало работы
Для локальной установки зависимостей, запустите следующие команды:
```
pip install uv
uv venv env --python 3.11
uv pip install -r pyproject.toml
```
Дополнительно:
```
uv pip list - все зависимости
uv pip uninstall <пакет> - удалить зависимости
uv pip sync pyproject.toml - синхронизировать зависимости
```

## Pre-commit
Установка pre-commit:
```
pre-commit install
```
[Указание директории](.pre-commit-config.yaml) в которых должны/не должны сработать pre-commit hooks:  
```
files: ^(apps/)
exclude: (?x).*/(alembic|vosk-model-small-ru-0.22)($|/.*)|
```

## Build команды
```
bash build/all.sh
bash build/local.sh

bash build/migrations_build.sh
bash build/migrations_activate.sh
```

## Файлы
Отправить .env на сервер:
```
scp /home/imblackmamba/projects/widgets/.env root@94.241.175.91:/root/projects/widgets
```
Отправить папку на сервер:
```
scp -r [источник] [получатель]
```