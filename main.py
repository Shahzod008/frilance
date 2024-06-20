from data import keyword_groups, channels_to_read, target_channels
from telethon import TelegramClient, events
from aiogram import Bot
from asyncio import Lock
import asyncio

lock = Lock()

client = TelegramClient(
    session="user",
    api_id=25518400,
    api_hash="78b80d815c74fec48abea67c7f238203",
    system_version='4.16.30-vxCUSTOM'
)

bot = Bot(token="6681696182:AAHgxahbzqOXe30c_58Z8kcASZIgB_qOQBs")


async def forward_message_to_channel(category, message_text, user_name):
    target_channel = target_channels.get(category)
    if target_channel:
        await bot.send_message(
            target_channel,
            text=f"{message_text}\n\nОт: @{user_name}",
            parse_mode='Markdown'
        )


@client.on(events.NewMessage(chats=channels_to_read))
async def handler(event):
    message_text = event.message.message
    user_name = event.sender.username

    if not user_name:
        return

    async with lock:
        for category, keywords in keyword_groups.items():
            if any(keyword.lower() in message_text.lower() for keyword in keywords):
                await forward_message_to_channel(category, message_text, user_name)


async def main():
    async with client:
        await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
