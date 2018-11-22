import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import random

Client = discord.Client()
client = commands.Bot(command_prefix ="!")

@client.event
async def on_ready():
    print("Bot is ready!")

@client.event
async def on_message(message):
    if message.content == "!cookie":
        await client.send_message(message.channel, ":cookie:")
    if message.author == client.user:
        return

    elif message.content.startswith('!guess'):
        await client.send_message(message.channel, 'Guess a number between 1 to 100')

        def guess_check(m):
            return m.content.isdigit()
        answer = random.randint(1, 100)
        guess = await client.wait_for_message(timeout=10, author=message.author, check=guess_check)
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await client.send_message(message.channel, fmt.format(answer))
            return
        if int(guess.content) == answer:
            await client.send_message(message.channel, 'You are right!')
            return
        else:
            while guess != answer:
                if int(guess.content) == answer:
                    await client.send_message(message.channel, 'You are right!')
                    return
                elif int(guess.content) < answer:
                    await client.send_message(message.channel, 'Your Guess was to Low')
                    guess = await client.wait_for_message(timeout=10, author=message.author, check=guess_check)
                elif int(guess.content) > answer:
                    await client.send_message(message.channel, 'Your Guess was to high')
                    guess = await client.wait_for_message(timeout=10, author=message.author, check=guess_check)
                else:
                    await client.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))

@client.event
async def on_member_join(member):
    server = member.server
    fmt = 'Welcome {0.mention} to a wellcome to the crew!'
    await client.send_message(server, fmt.format(member))

client.run("NTE0MjUyMTI3NDQ3Njc5MDIx.DtcbtA.pfV7ZCrH1Q5x9elQJN_JI5GavqY")
