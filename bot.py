#!/usr/bin/env python3.6
# Work with Python 3.6

import json
import discord
from discord.ext.commands import Bot

with open("auth.json") as data_file:
    auth = json.load(data_file)
with open("exceptions.json") as data_file:
    data = json.load(data_file)

TOKEN = auth["token"]
BOT_PREFIX = "!"

client = Bot(BOT_PREFIX)


@client.event
async def on_message(msg):
    # We do not want the bot to respond to Bots or Webhooks
    if msg.author.bot:
        return
    # We want the bot to not answer to messages that have no content
    # (example only attachment messages)
    if not msg.content:
        return
    # Bot ignore all system messages
    if msg.type is not discord.MessageType.default:
        return

    # Bot ignore messages from special roles
    if not (
        "Core-Team" in [role.name for role in msg.author.roles]
        or "Support-Team" in [role.name for role in msg.author.roles]
        or "Contributors" in [role.name for role in msg.author.roles]
    ):
        message = f"{data['default']}"
        await client.send_message(msg.channel, message)
        return

    args = msg.content.split()
    for check in args:
        for link in data["links"]:
            if check == link:
                return
        if (len(check) >= 30 and check[:29] == "https://discordapp.com/invite/"):
            await client.delete_message(msg)


@client.event
async def on_ready():
    print(f"Logged in as: {client.user.name} {{{client.user.id}}}")

client.run(TOKEN)
