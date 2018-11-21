import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import irc

Client = discord.Client()
client = commands.Bot(command_prefix ="!")

@client.event
async def on_ready():
    print("Bot is ready!")

@client.event
async def on_message(message):
    if message.content == "cookie":
        await client.send_message(message.channel, "cookie")



client.run("NTE0MjUyMTI3NDQ3Njc5MDIx.DtT28g.DlseHl3VHb512ENVJ0jZD7Pt0tg")
