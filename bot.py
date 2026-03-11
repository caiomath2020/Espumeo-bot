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
    member = member or ctx.author

    embed = discord.Embed(title=f"Informações de {member}", color=0x00ff00)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Status", value=str(member.status).title(), inline=True)
    embed.add_field(name="Top Role", value=member.top_role, inline=True)
    embed.add_field(name="Cargos", value=", ".join([role.name for role in member.roles if role.name != "@everyone"]), inline=False)
    embed.add_field(name="Entrou no servidor", value=member.joined_at.strftime("%d/%m/%Y %H:%M"), inline=True)
    embed.add_field(name="Conta criada em", value=member.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)

    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild

    membros = []
    async for m in guild.fetch_members(limit=None):
        membros.append(m)

    online = len([m for m in membros if m.status != discord.Status.offline])
    total_canais = len(guild.channels)
    total_cargos = len(guild.roles)
    dono = guild.owner
    criacao = guild.created_at.strftime("%d/%m/%Y %H:%M")

    embed = discord.Embed(title=f"Informações de {guild.name}", color=0x3498db)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    embed.add_field(name="Dono", value=dono, inline=True)
    embed.add_field(name="Membros Totais", value=total_membros, inline=True)
    embed.add_field(name="Membros Online", value=online, inline=True)
    embed.add_field(name="Canais", value=total_canais, inline=True)
    embed.add_field(name="Cargos", value=total_cargos, inline=True)
    embed.add_field(name="Servidor criado em", value=criacao, inline=False)

    await ctx.send(embed=embed)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

import os
print(os.getenv("TOKEN"))
bot.run(os.getenv("TOKEN"))

