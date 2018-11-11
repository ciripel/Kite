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
    for ex_rol in data["except_roles"]:
        if ex_rol in [role.name for role in msg.author.roles]:
            return
    # BOT is ignoring exceptions
    # This is usefull if the exception is containing the forbidden word (expresion)
    for ex_link in data["except_links"]:
        if ex_link in msg.content:
            return
    # Bot is parsing all the words (expresions) list and check if the message is
    # containing any of them and delete the messages that contain them
    for ban_word in data["banned_words"]:
        if ban_word in msg.content:
            await client.delete_message(msg)
            # return is used here to not have double words and call a delete_message(deleted_message)
            return


@client.event
async def on_ready():
    print(f"Logged in as: {client.user.name} {{{client.user.id}}}")


client.run(TOKEN)
