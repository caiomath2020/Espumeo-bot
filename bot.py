import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot ligado como {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")
@bot.command()
async def limpar(ctx, quantidade: int):
    await ctx.channel.purge(limit=quantidade)
import os
bot.run(os.getenv("TOKEN"))