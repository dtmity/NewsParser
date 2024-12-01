import feedparser
from datetime import datetime, timedelta, timezone


def news_pars(delta, keywords={'Добро'}):
    bd_mess = []
    sources = {('https://lenta.ru/rss/news', 'lenta'),
               ('https://russian.rt.com/rss', 'rt'),
               ('https://www.vedomosti.ru/rss/news.xml', 'ведомости'),
               ('https://ria.ru/export/rss2/index.xml', 'ria')}

    for url, name in sources:
        rss = feedparser.parse(url)
        yesterday = datetime.now(timezone.utc) - delta

        for item in rss.entries:
            pub_date = datetime.strptime(item.published, '%a, %d %b %Y %H:%M:%S %z')
            if pub_date > yesterday:
                if any(keyword in item.title for keyword in keywords):
                    pub_date_str = pub_date.strftime('%H:%M:%S \n%d.%m.%Y ')
                    bd_mess.append(f'{item.title} \n\n{pub_date_str} \n[Источник: {name}]({item.link})')
    return bd_mess
