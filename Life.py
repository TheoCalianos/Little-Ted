import asyncio
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import time
import code
import random
bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), description='A playlist example for discord.py')
class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

class Music:
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice
    @commands.command(pass_context=True, no_pm=True)
    async def cookie(self, ctx):
        await self.bot.say(":cookie:")
    @commands.command(pass_context=True, no_pm=True)
    async def guess(ctx):
        def guess_check(m):
            return m.content.isdigit()
        await bot.say('Guess a number between 1 to 100')
        answer = random.randint(1, 100)
        guess = await bot.wait_for_message(timeout=10)
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await bot.say(fmt.format(answer))
            return
        if int(guess.content) == answer:
            await bot.say('You are right!')
            return
        else:
            while guess != answer:
                if int(guess.content) == answer:
                    await bot.say('You are right!')
                    return
                elif int(guess.content) < answer:
                    await bot.say('Your Guess was to Low')
                    guess = await bot.wait_for_message(timeout=10, check=guess_check)
                elif int(guess.content) > answer:
                    await bot.say('Your Guess was to high')
                    guess = await bot.wait_for_message(timeout=10, check=guess_check)
                else:
                    await bot.say('Sorry. It is actually {}.'.format(answer))
    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('You are not in a voice channel.')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True
bot.add_cog(Music(bot))
@bot.event
async def on_ready():
    print("Bot is ready!")
@bot.event
async def on_member_join(member):
    server = member.server
    fmt = 'Welcome {0.mention} to a wellcome to the crew!'
    await bot.send_message(server, fmt.format(member))

bot.run("NTE0MjUyMTI3NDQ3Njc5MDIx.Dt5aMw.t7F76fGerGYIZy2_wLQ7bExZsp0")
