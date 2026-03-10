import discord
from discord.ext import commands
import time

spam_tracker = {}
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot ligado como {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user = message.author.id
    now = time.time()

    if user not in spam_tracker:
        spam_tracker[user] = []

    spam_tracker[user].append((message, now))

    spam_tracker[user] = [(msg, t) for msg, t in spam_tracker[user] if now - t < 5]

    if len(spam_tracker[user]) >= 5:
        for msg, _ in spam_tracker[user]:
            try:
                await msg.delete()
            except discord.Forbidden:
                print(f"Não consegui apagar mensagem de {message.author}")
            except discord.NotFound:
                pass
        await message.channel.send(f"{message.author.mention} pare de spammar.")
        spam_tracker[user].clear()
        return

    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def limpar(ctx, quantidade: int):
    await ctx.channel.purge(limit=quantidade)

import os
print(os.getenv("TOKEN"))
bot.run(os.getenv("TOKEN"))
