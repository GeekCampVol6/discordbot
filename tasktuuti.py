import discord
from discord.ext import commands, tasks
from datetime import datetime, time
import json

# トークン取得
TOKEN = "MTEyOTY0ODA0OTc4Njk5NDc2OQ.GL37sa.OIrwRDzr5SO6Sm0FDIVQy_skY3ktbpzY_iSdBI"
CHANNEL_ID = 1129649056625475688
# JSONのファイルパスを取得
JSON_FILE_PATH = "data.json"
ITEM_FILE_PATH = "item.json"
# 通知時間を取得
NOTIFICATION_TIME = time(hour=0, minute=0, second=0)

# Botの起動
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents,
                      shard_count=3, shard_id=0)

# コマンドの作成


@tasks.loop(minutes=1440)
async def loop():
    now = datetime.now()
    notification_time = datetime.combine(now.date(), NOTIFICATION_TIME)

    with open(ITEM_FILE_PATH, 'r', encoding="utf-8") as item_file:
        datas = json.load(item_file)
        flag = 0

        for data in datas:
            date_objs = datetime.strptime(data['date'], '%Y-%m-%d')

            if now.date() == date_objs.date() and now.time() >= notification_time.time() and flag == 0:
                messages = f"今日持ってくる持ち物"
                channel = client.get_channel(CHANNEL_ID)
                await channel.send(messages)
                flag = 1

            for detail in data['detail']:
                if now.date() == date_objs.date() and now.time() >= notification_time.time():
                    itemmsg = f"\n{detail['subject']}:{detail['object']}"
                    channel = client.get_channel(CHANNEL_ID)
                    await channel.send(itemmsg)

    with open(JSON_FILE_PATH, 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)
        flags = 0
        for item in data['detail']:
            date = datetime.strptime(item['date'], '%Y-%m-%d')

            if now.date() == date.date() and now.time() >= notification_time.time() and flags == 0:
                taskmsg = f"\n\n今日提出の課題"
                channel = client.get_channel(CHANNEL_ID)
                await channel.send(taskmsg)
                flags = 1

            # 現在時刻が9:00以降であれば通知する
            if now.date() == date.date() and now.time() >= notification_time.time():
                # メッセージを作成
                message = f"\n【科目名称:{item['subject']}】\n課題名称:{item['themaname']} \n納期:{item['date']} \n担当教官:{item['teachername']} \n課題詳細:{item['detail']} \n課題種類:{item['status']}\n"
                channel = client.get_channel(CHANNEL_ID)
                await channel.send(message)


# Botの起動とDiscordサーバーへの接続


@client.event
async def on_ready():
    loop.start()

client.run(TOKEN)
