# NewsParser
 Агрегатор источников новостей

## Описание
Это бот — агрегатор новостей из различных источников

1. \help — показать помощь
2. \keys <ключевые слова через запятую>  — отправить запрос по ключевым словам
3. \set_delta — выбрать за какой отрезок времени искать новости

@dtmity — по любым вопросам работы бота

## Установка

1. Клонируйте репозиторий: `git clone https://github.com/dtmity/NewsParser.git`
2. Установите нужные пакеты: `pip install -r requirements.txt`

## Запуск

1. В файле `config.py` введите токен своего бота
2. Для возможности парсинга по телеграм-каналам там же нужно ввести свои api_id и api_hash
3. Напишите в терминал `python main.py` для начала работы бота
4. Во время первого запроса к телеграм-каналам, у вас могут попросить пройти авторизацию

## Скриншоты

![Скрин 1](https://github.com/dtmity/NewsParser/raw/main/shots/1.png)

![Скрин 2](https://github.com/dtmity/NewsParser/raw/main/shots/2.png)

![Скрин 3](https://github.com/dtmity/NewsParser/raw/main/shots/3.png)
