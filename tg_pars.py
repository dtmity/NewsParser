from telethon import TelegramClient, sync, errors
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
from datetime import datetime, timedelta, timezone
import time
from config import api_id, api_hash
from sources import channels_name

import asyncio


def tg_pars(delta, keywords):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    client = TelegramClient('sess', api_id, api_hash)

    since_datetime = datetime.now(timezone.utc) - delta
    bd_mess = []

    try:
        client.start()
    except errors.RPCError as e:
        print(f"Ошибка подключения к Telegram: {e}")
        return -1
    except Exception as e:
        print(f"Непредвиденная ошибка при запуске клиента: {e}")
        return -1

    for channel_name in channels_name:
        try:
            target_channel = client.get_entity(channel_name)
        except errors.RPCError as e:
            print(f"Ошибка при получении сущности канала {channel_name}: {e}")
            continue
        except Exception as e:
            print(f"Непредвиденная ошибка при получении сущности канала {channel_name}: {e}")
            continue

        try:
            for message in client.iter_messages(target_channel):
                if message.date < since_datetime:
                    break

                try:
                    if message.text and any(keyword in message.text for keyword in keywords):
                        pub_date = message.date.strftime('%H:%M:%S \n%d.%m.%Y')
                        text = message.text.split('\n')[0][:200]
                        bd_mess.append(
                            f"{text} \n {pub_date} \n https://t.me/c/{target_channel.id}/{message.id}")
                except AttributeError as e:
                    print(f"Ошибка при обработке сообщения: {e}")
                except Exception as e:
                    print(f"Непредвиденная ошибка при обработке сообщения: {e}")

        except errors.RPCError as e:
            print(f"Ошибка при получении сообщений канала {channel_name}: {e}")
            continue
        except Exception as e:
            print(f"Непредвиденная ошибка при получении сообщений канала {channel_name}: {e}")
            continue

    try:
        client.disconnect()
    except Exception as e:
        print(f"Ошибка при отключении клиента: {e}")

    return bd_mess if bd_mess else -1
