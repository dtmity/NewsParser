from telethon import TelegramClient, sync
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
from datetime import datetime, timedelta, timezone
import time
from config import api_id, api_hash

import asyncio


def tg_pars(delta, keywords):
    channels_name = {'oldlentach', 'rian_ru', 'breakingmash'}

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    client = TelegramClient('sess', api_id, api_hash)

    since_datetime = datetime.now(timezone.utc) - delta

    bd_mess = []
    if client.start():
        for channel_name in channels_name:
            target_channel = client.get_entity(channel_name)
            for message in client.iter_messages(target_channel):
                if message.date < since_datetime:
                    break
                if any(keyword in message.text for keyword in keywords):
                    pub_date = message.date.strftime('%H:%M:%S \n%d.%m.%Y')
                    text = message.text.split('\n')[0][:200]
                    bd_mess.append(
                        f"{text} \n {pub_date} \n https://t.me/c/{target_channel.id}/{message.id}")

        return bd_mess
    else:
        return -1
