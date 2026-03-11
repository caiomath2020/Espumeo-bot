import discord
from discord.ext import commands
import time

spam_tracker = {}
intents = discord.Intents.default()
intents.messages = True
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

    spam_tracker[user] = [(msg, t) for msg, t in spam_tracker[user] if now - t < 4]

    if len(spam_tracker[user]) >= 5:
        for msg, _ in spam_tracker[user]:
            try:
                await msg.delete()
            except discord.Forbidden:
                print(f"Não consegui apagar mensagem de {message.author}")
            except discord.NotFound:
                pass
        await message.channel.send(f"{message.author.mention} PARA DE SPAMMAR DOENTE")
        spam_tracker[user].clear()
        return

    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def limpar(ctx, quantidade: int):
    await ctx.channel.purge(limit=quantidade)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author  # se não mencionar, pega quem chamou o comando

    embed = discord.Embed(title=f"Informações de {member}", color=0x00ff00)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Status", value=str(member.status).title(), inline=True)
    embed.add_field(name="Top Role", value=member.top_role, inline=True)
    embed.add_field(name="Cargos", value=", ".join([role.name for role in member.roles if role.name != "@everyone"]), inline=False)
    embed.add_field(name="Entrou no servidor", value=member.joined_at.strftime("%d/%m/%Y %H:%M"), inline=True)
    embed.add_field(name="Conta criada em", value=member.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)

    await ctx.send(embed=embed)

import os
print(os.getenv("TOKEN"))
bot.run(os.getenv("TOKEN"))








