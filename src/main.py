import discord
from discord.ext import commands
import random
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} está online!')
    await bot.change_presence(activity=discord.Game(name="Estou aqui para ajudar!"))

@bot.command(name="saudar")
async def saudar(ctx):
    await ctx.send(f"Olá, {ctx.author.mention}! Como posso ajudar hoje?")

@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! Latência: {latency}ms")

@bot.command(name="hora")
async def hora(ctx):
    agora = datetime.now().strftime("%H:%M:%S")
    await ctx.send(f"A hora atual é: {agora}")

@bot.command(name="pergunta")
async def pergunta(ctx):
    respostas = ["Sim!", "Não!", "Talvez.", "Pergunte mais tarde.", "Com certeza!", "Não posso responder isso agora."]
    resposta = random.choice(respostas)
    await ctx.send(f"{resposta}")

@bot.command(name="dm")
@commands.is_owner()
async def dm(ctx, membro: discord.Member, *, conteudo):
    try:
        await membro.send(conteudo)
        await ctx.send(f"Mensagem enviada para {membro.mention}.")
    except discord.Forbidden:
        await ctx.send(f"Não consegui enviar a mensagem para {membro.mention}. :(")

@bot.command(name="limpar")
@commands.has_permissions(manage_messages=True)
async def limpar(ctx, quantidade: int = 10):
    await ctx.channel.purge(limit=quantidade)
    await ctx.send(f"{quantidade} mensagens apagadas.", delete_after=5)

@bot.command(name="avatar")
async def avatar(ctx, membro: discord.Member = None):
    membro = membro or ctx.author
    await ctx.send(f"Aqui está o avatar de {membro.mention}: {membro.avatar.url}")

@bot.command(name="servidor")
async def servidor(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"Informações do servidor {guild.name}", color=discord.Color.blue())
    embed.add_field(name="ID do Servidor", value=guild.id)
    embed.add_field(name="Dono", value=guild.owner)
    embed.add_field(name="Membros", value=guild.member_count)
    embed.add_field(name="Criado em", value=guild.created_at.strftime("%d/%m/%Y"))
    await ctx.send(embed=embed)

@bot.command(name="banir")
@commands.has_permissions(ban_members=True)
async def banir(ctx, membro: discord.Member, *, motivo=None):
    await membro.ban(reason=motivo)
    await ctx.send(f"{membro.mention} foi banido. Motivo: {motivo}")

@bot.command(name="desbanir")
@commands.has_permissions(ban_members=True)
async def desbanir(ctx, id_usuario: int):
    user = await bot.fetch_user(id_usuario)
    await ctx.guild.unban(user)
    await ctx.send(f"{user.name} foi desbanido!")

@bot.command(name="userinfo")
async def userinfo(ctx, membro: discord.Member = None):
    membro = membro or ctx.author
    embed = discord.Embed(title=f"Informações do usuário: {membro.name}", color=discord.Color.green())
    embed.add_field(name="ID", value=membro.id)
    embed.add_field(name="Nome", value=membro.display_name)
    embed.add_field(name="Conta criada em", value=membro.created_at.strftime("%d/%m/%Y"))
    embed.add_field(name="Entrou no servidor em", value=membro.joined_at.strftime("%d/%m/%Y"))
    embed.set_thumbnail(url=membro.avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="sorteio")
@commands.has_permissions(administrator=True)
async def sorteio(ctx, premio: str):
    msg = await ctx.send(f"Sorteio iniciado! Reaja com 🎉 para participar do sorteio de {premio}!")
    await msg.add_reaction("🎉")
    await bot.wait_for("reaction_add", check=lambda reaction, user: reaction.emoji == "🎉" and reaction.message.id == msg.id)
    
    participantes = []
    async for user in msg.reactions[0].users():
        if user != bot.user:
            participantes.append(user)
    
    if participantes:
        vencedor = random.choice(participantes)
        await ctx.send(f"🎉 Parabéns, {vencedor.mention}! Você ganhou o prêmio: {premio}!")
    else:
        await ctx.send("Ninguém participou do sorteio.")

@bot.command(name="fato")
async def fato(ctx):
    fatos = [
        "Os golfinhos dormem com um olho aberto.",
        "A Terra não é perfeitamente redonda; é um pouco achatada nos polos.",
        "A estrela-do-mar não tem cérebro.",
        "O mel nunca estraga.",
        "O coração de um camarão fica na sua cabeça."
    ]
    fato = random.choice(fatos)
    await ctx.send(f"Fato interessante: {fato}")

@bot.command(name="moeda")
async def moeda(ctx):
    resultado = random.choice(["Cara", "Coroa"])
    await ctx.send(f"A moeda caiu em: {resultado}")

@bot.command(name="dado")
async def dado(ctx):
    numero = random.randint(1, 6)
    await ctx.send(f"Você rolou o dado e saiu: {numero}")

@bot.command(name="lembrete")
async def lembrete(ctx, tempo: int, *, mensagem):
    await ctx.send(f"Lembrete definido para {tempo} segundos.")
    await asyncio.sleep(tempo)
    await ctx.send(f"Lembrete: {mensagem}")

@bot.command(name="clima")
async def clima(ctx, cidade: str):
    climas = ["ensolarado", "nublado", "chuvoso", "tempestuoso", "nevoeiro"]
    clima_hoje = random.choice(climas)
    await ctx.send(f"O clima em {cidade} hoje está: {clima_hoje}")

bot.run("ur bot token")
