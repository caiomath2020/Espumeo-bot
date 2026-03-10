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
        return  # ignora bots

    # ⚡ Processa comandos primeiro para evitar respostas duplicadas
    await bot.process_commands(message)

    # ----- Lógica de anti-spam -----
    user = message.author.id
    now = time.time()

    if user not in spam_tracker:
        spam_tracker[user] = []

    # guarda a mensagem e o horário
    spam_tracker[user].append((message, now))

    # mantém apenas mensagens dos últimos 5 segundos
    spam_tracker[user] = [(msg, t) for msg, t in spam_tracker[user] if now - t < 5]

    # se enviar 5 ou mais mensagens nesse período, apaga todas
    if len(spam_tracker[user]) >= 5:
        for msg, _ in spam_tracker[user]:
            try:
                await msg.delete()
            except discord.Forbidden:
                print(f"Não consegui apagar mensagem de {message.author}")
            except discord.NotFound:
                pass  # mensagem já apagada
        await message.channel.send(f"{message.author.mention} pare de spammar.")
        spam_tracker[user].clear()
        return  # evita processar comandos novamente

# ----- Comandos -----
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def limpar(ctx, quantidade: int):
    await ctx.channel.purge(limit=quantidade)

import os
print(os.getenv("TOKEN"))
bot.run(os.getenv("TOKEN"))
