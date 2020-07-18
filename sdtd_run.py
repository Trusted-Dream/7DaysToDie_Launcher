#!/bin/env python
import discord
import threading
import os
import re
import time
import subprocess as prc
from Sdtd import command

API = "API KEY"
ADMIN = "admin"
SubADMIN = "subadmin"

client = discord.Client()
#@client.event
#async def on_ready():
#    print('Logged in as')
#    print(client.user.name)
#    print(client.user.id)
#    print('------')

@client.event
async def on_message(message):
    if message.author.name == (ADMIN) or message.author.name == (SubADMIN):
        cmd = command.SDTD()
        if message.content.startswith('/help'):
            cmdhelp = cmd.command_help()
            await message.channel.send(cmdhelp)

        elif message.content.startswith('/member'):
            await message.channel.send(cmd.player_joined_check())

        elif message.content.startswith('/server-start'):
            timemsg = time.strftime("%Y/%m/%d %H:%M:%S ", time.strptime(time.ctime()))
            await message.channel.send(timemsg + "--- サーバを起動します。(起動には5分程かかる場合があります。)")
            thread = threading.Thread(target=cmd.start)
            thread.start()

        elif message.content.startswith('/server-stop'):
            timemsg = time.strftime("%Y/%m/%d %H:%M:%S ", time.strptime(time.ctime()))
            await message.channel.send(timemsg + "--- サーバを停止します。")
            thread = threading.Thread(target=cmd.stop)
            thread.start()

        elif message.content.startswith('/server-restart'):
            timemsg = time.strftime("%Y/%m/%d %H:%M:%S ", time.strptime(time.ctime()))
            await message.channel.send(timemsg + "--- サーバを再起動します。")
            thread = threading.Thread(target=cmd.stop)
            thread.start()
            time.sleep(15)
            timemsg = time.strftime("%Y/%m/%d %H:%M:%S ", time.strptime(time.ctime()))
            await message.channel.send(timemsg + "--- サーバを起動します。(起動には5分程かかる場合があります。)")
            thread = threading.Thread(target=cmd.start)
            thread.start()

        elif message.content.startswith('/server-status'):
            timemsg = time.strftime("%Y/%m/%d %H:%M:%S ", time.strptime(time.ctime()))
            await message.channel.send(timemsg + "--- サーバの状況を表示します。")
            await message.channel.send(cmd.status())

client.run(API)
