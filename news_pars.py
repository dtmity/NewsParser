import feedparser
from datetime import datetime, timedelta, timezone
from sources import sources


def news_pars(delta, keywords={'Добро'}):
    bd_mess = []

    for url, name in sources:
        try:
            rss = feedparser.parse(url)
        except Exception as e:
            print(f"Ошибка при парсинге URL {url}: {e}")
            continue

        try:
            yesterday = datetime.now(timezone.utc) - delta
        except Exception as e:
            print(f"Ошибка при вычислении времени отсечения: {e}")
            return -1

        for item in rss.entries:
            try:
                if not all(hasattr(item, attr) for attr in ['published', 'title', 'link']):
                    print(f"Пропущено сообщение из-за отсутствия одного из обязательных атрибутов (published, title, link)")
                    continue

                try:
                    pub_date = datetime.strptime(item.published, '%a, %d %b %Y %H:%M:%S %z')
                except ValueError as e:
                    print(f"Ошибка преобразования даты {item.published} для источника {url}: {e}")
                    continue

                if pub_date > yesterday:
                    try:
                        if any(keyword in item.title for keyword in keywords):
                            pub_date_str = pub_date.strftime('%H:%M:%S \n%d.%m.%Y ')
                            bd_mess.append(f'{item.title} \n\n{pub_date_str} \n[Источник: {name}]({item.link})')
                    except Exception as e:
                        print(f"Ошибка при обработке сообщения из источника {url}: {e}")
            except Exception as e:
                print(f"Общая ошибка при обработке записи из источника {url}: {e}")

    return bd_mess if bd_mess else -1
