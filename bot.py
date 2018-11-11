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
    if (
        "Core-Team" in [role.name for role in msg.author.roles]
        or "Support-Team" in [role.name for role in msg.author.roles]
        or "Contributors" in [role.name for role in msg.author.roles]
        or "Team" in [role.name for role in msg.author.roles]
    ):
        return

    for link in data["links"]:
        if link in msg.content:
            return
    if "https://discordapp.com/invite/" in msg.content:
        await client.delete_message(msg)


@client.event
async def on_ready():
    print(f"Logged in as: {client.user.name} {{{client.user.id}}}")


client.run(TOKEN)
