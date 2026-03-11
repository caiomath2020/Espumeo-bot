# ---------- COMANDO !USERINFO (ajustado) ----------
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    # garante pegar o status real
    member = await ctx.guild.fetch_member(member.id)

    embed = discord.Embed(title=f"Informações de {member}", color=0x00ff00)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Status", value=str(member.status).title(), inline=True)
    embed.add_field(name="Top Role", value=member.top_role, inline=True)
    embed.add_field(
        name="Cargos",
        value=", ".join([role.name for role in member.roles if role.name != "@everyone"]),
        inline=False,
    )
    embed.add_field(name="Entrou no servidor", value=member.joined_at.strftime("%d/%m/%Y %H:%M"), inline=True)
    embed.add_field(name="Conta criada em", value=member.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)

    await ctx.send(embed=embed)


# ---------- COMANDO !SERVERINFO (ajustado) ----------
@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild

    # pega todos os membros com fetch para status real
    membros = []
    async for m in guild.fetch_members(limit=None):
        membros.append(m)

    total_membros = len(membros)
    online = len([m for m in membros if m.status != discord.Status.offline])
    total_canais = len(guild.channels)
    total_cargos = len(guild.roles)
    dono = guild.owner if guild.owner else "Desconhecido"
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
