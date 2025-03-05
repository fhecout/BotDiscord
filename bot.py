import discord
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from discord.ext import commands
import http.client
import json
import yt_dlp
import random

load_dotenv()

# Configurações
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# Nome de usuário
INSTAGRAM_USER = "joaoluzx"
YOUTUBE_CHANNEL_ID = "UCEWqU3-iOpqqbaoTju6by3Q"
TIKTOK_USER = "joaoluzx"


# Configurar Intents
intents = discord.Intents.default()
intents.message_content = True
# Criar o bot
bot = commands.Bot(command_prefix="!", intents=intents)


queue = []


# Evento de boas-vindas
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="entradas-e-saidas")  # Alterar para o nome do canal desejado
    if channel:
        await channel.send(f"🎉 Bem-vindo ao servidor, {member.mention}! Esperamos que se divirta. 🚀")

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Converte de segundos para milissegundos
    await ctx.send(f"🏓 Pong! Latência: {latency}ms")
    

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"ℹ️ Informações do Servidor: {guild.name}", color=0x3498db)
    embed.add_field(name="👥 Membros", value=guild.member_count, inline=True)
    embed.add_field(name="📂 Canais", value=len(guild.channels), inline=True)
    embed.add_field(name="💎 Boosts", value=guild.premium_subscription_count, inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)  # Mostra o ícone do servidor

    await ctx.send(embed=embed)


@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="geral")  # Altere para o nome do canal certo
    if channel:
        await channel.send(f"😢 {member.name} saiu do servidor. Sentiremos sua falta!")



@bot.command()
async def enquete(ctx, pergunta: str, *opcoes):
    if len(opcoes) < 2:
        await ctx.send("❌ Você deve fornecer pelo menos duas opções para a enquete.")
        return

    opcoes_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
    
    if len(opcoes) > len(opcoes_emojis):
        await ctx.send("❌ Número máximo de opções é 6.")
        return

    embed = discord.Embed(title="📊 Enquete", description=pergunta, color=0xffc107)
    descricao = "\n".join([f"{opcoes_emojis[i]} {opcoes[i]}" for i in range(len(opcoes))])
    embed.add_field(name="Opções:", value=descricao, inline=False)
    
    mensagem = await ctx.send(embed=embed)
    
    for i in range(len(opcoes)):
        await mensagem.add_reaction(opcoes_emojis[i])
        
        
        


### 🔧 Baixar FFmpeg automaticamente ###
FFMPEG_PATH = "C:/FFmpeg/ffmpeg.exe"


def baixar_ffmpeg():
    """Baixa FFmpeg automaticamente se não estiver presente."""
    if not os.path.exists(FFMPEG_PATH):
        print("🔄 Baixando FFmpeg, aguarde...")
        response = requests.get(FFMPEG_URL)
        with open(FFMPEG_PATH, "wb") as file:
            file.write(response.content)
        print("✅ FFmpeg baixado com sucesso!")


### 🔊 ENTRAR AUTOMATICAMENTE AO TOCAR UMA MÚSICA ###
@bot.command()
async def tocar(ctx, *, url):
    """ Adiciona uma música à fila e toca automaticamente """
    if ctx.author.voice is None:
        await ctx.send("❌ Você precisa estar em um canal de voz para tocar música!")
        return
    
    queue.append(url)  # Adiciona a música à fila

    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()  # Entra no canal de voz automaticamente

    if not ctx.voice_client.is_playing():
        await play_next(ctx)  # Toca imediatamente se a fila estava vazia


async def play_next(ctx):
    """ Toca a próxima música da fila """
    if not queue:
        await ctx.send("✅ Fila de músicas vazia, saindo do canal!")
        await ctx.voice_client.disconnect()
        return

    url = queue.pop(0)  # Pega a próxima música da fila

    await ctx.send(f"🎶 Tocando agora: {url}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']

    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    ctx.voice_client.play(
    discord.FFmpegPCMAudio(audio_url, **ffmpeg_options, executable=FFMPEG_PATH),
    after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop)
    )


### ⏸️ COMANDO PARA PAUSAR A MÚSICA ###
@bot.command()
async def pausar(ctx):
    """ Pausa a música atual """
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ Música pausada.")
    else:
        await ctx.send("❌ Nenhuma música está tocando.")


### ▶️ COMANDO PARA RETOMAR A MÚSICA ###
@bot.command()
async def retomar(ctx):
    """ Retoma a música pausada """
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Música retomada.")
    else:
        await ctx.send("❌ Nenhuma música está pausada.")


### ⏭️ COMANDO PARA PULAR PARA A PRÓXIMA MÚSICA ###
@bot.command()
async def pular(ctx):
    """ Pula a música atual e toca a próxima da fila """
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()  # Para a música atual, chamando automaticamente play_next(ctx)
        await ctx.send("⏩ Música pulada! Tocando a próxima da fila...")
    else:
        await ctx.send("❌ Nenhuma música está tocando para ser pulada.")


### ⏹️ COMANDO PARA PARAR E SAIR DO CANAL ###
@bot.command()
async def sair(ctx):
    """ Sai do canal de voz e limpa a fila """
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        queue.clear()
        await ctx.send("👋 Saí do canal de voz!")
    else:
        await ctx.send("❌ Não estou em um canal de voz.")


### 📜 COMANDO PARA MOSTRAR A FILA DE MÚSICAS ###
@bot.command()
async def fila(ctx):
    """ Mostra as músicas na fila """
    if queue:
        await ctx.send("📜 *Fila de músicas:*\n" + "\n".join(queue))
    else:
        await ctx.send("✅ A fila está vazia.")






@bot.command()
async def ajuda(ctx):
    embed = discord.Embed(
        title="📖 Lista de Comandos do Bot",
        description="Aqui estão todos os comandos disponíveis:",
        color=0x3498db
    )

    # 🎮 Comandos Gerais
    embed.add_field(name="⚡ !ping", value="Verifica a latência do bot.", inline=False)
    embed.add_field(name="🖼️ !avatar @usuário", value="Exibe o avatar de um usuário.", inline=False)
    embed.add_field(name="🎲 !dado [lados]", value="Rola um dado de X lados (padrão: 6).", inline=False)
    embed.add_field(name="🪙 !moeda", value="Joga cara ou coroa.", inline=False)
    embed.add_field(name="👤 !userinfo @usuário", value="Mostra informações sobre um usuário.", inline=False)
    embed.add_field(name="🧹 !limpar [quantidade]", value="Apaga mensagens (apenas admins).", inline=False)

    # 📊 Comandos de Interação
    embed.add_field(name="📊 !enquete <pergunta> <opção1> <opção2> ...", value="Cria uma enquete com até 6 opções.", inline=False)
    embed.add_field(name="🎉 !sorteio", value="Sorteia um membro aleatório do servidor.", inline=False)
    embed.add_field(name="📈 !seguidores", value="Mostra os seguidores do Instagram, YouTube e TikTok.", inline=False)

    # 🎵 Comandos de Música
    embed.add_field(name="🎶 !tocar <link>", value="Adiciona uma música à fila e toca automaticamente.", inline=False)
    embed.add_field(name="⏸ !pausar", value="Pausa a música atual.", inline=False)
    embed.add_field(name="▶️ !retomar", value="Retoma a música pausada.", inline=False)
    embed.add_field(name="⏩ !pular", value="Pula a música atual e toca a próxima da fila.", inline=False)
    embed.add_field(name="📜 !fila", value="Exibe as músicas na fila.", inline=False)
    embed.add_field(name="⏹ !sair", value="Para a música e sai do canal de voz.", inline=False)

    embed.set_footer(text="Use o prefixo '!' antes de cada comando.")

    await ctx.send(embed=embed)




@bot.command()
async def avatar(ctx, membro: discord.Member = None):
    membro = membro or ctx.author  # Se não for mencionado, pega o próprio autor
    embed = discord.Embed(title=f"🖼️ Avatar de {membro.name}", color=0x00ff00)
    embed.set_image(url=membro.avatar.url)  # Exibe o avatar do usuário
    await ctx.send(embed=embed)


@bot.command()
async def sorteio(ctx):
    membros = [m for m in ctx.guild.members if not m.bot]  # Evita escolher bots
    vencedor = random.choice(membros)
    await ctx.send(f"🎉 Parabéns, {vencedor.mention}! Você foi sorteado! 🎊")
    
    
@bot.command()
async def moeda(ctx):
    resultado = random.choice(["🪙 Cara!", "🪙 Coroa!"])
    await ctx.send(f"{ctx.author.mention}, o resultado foi: {resultado}")


@bot.command()
async def dado(ctx, lados: int = 6):
    if lados < 2:
        await ctx.send("🎲 O dado precisa ter pelo menos 2 lados!")
        return
    
    resultado = random.randint(1, lados)
    await ctx.send(f"🎲 {ctx.author.mention} rolou um dado de {lados} lados e tirou *{resultado}*!")


@bot.command()
async def userinfo(ctx, membro: discord.Member = None):
    membro = membro or ctx.author  # Se não mencionar ninguém, mostra informações do próprio autor
    embed = discord.Embed(title=f"👤 Informações de {membro.name}", color=0x1abc9c)
    embed.set_thumbnail(url=membro.avatar.url)
    embed.add_field(name="📛 Nome:", value=membro.name, inline=True)
    embed.add_field(name="🆔 ID:", value=membro.id, inline=True)
    embed.add_field(name="📅 Entrou no Servidor:", value=membro.joined_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="🔰 Cargo Mais Alto:", value=membro.top_role.mention, inline=True)
    
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpar(ctx, quantidade: int = 5):
    if quantidade < 1:
        await ctx.send("❌ A quantidade de mensagens a serem apagadas deve ser maior que 0.")
        return
    
    await ctx.channel.purge(limit=quantidade + 1)  # +1 para também apagar o comando
    await ctx.send(f"🗑️ {quantidade} mensagens foram apagadas!", delete_after=3)




        

# Função para obter seguidores do YouTube via API do Google
def get_youtube_followers():
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={YOUTUBE_CHANNEL_ID}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            return data["items"][0]["statistics"]["subscriberCount"]
    return "Erro"

# Função para obter seguidores do Instagram usando a nova API
def get_instagram_followers():
    url = "https://rocketapi-for-instagram.p.rapidapi.com/instagram/user/get_info"
    payload = {"username": INSTAGRAM_USER}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "rocketapi-for-instagram.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        data = response.json()
        
        # Acessa o número de seguidores
        followers = data["response"]["body"]["data"]["user"]["edge_followed_by"]["count"]
        return followers
    except Exception as e:
        print(f"Erro na requisição do Instagram: {e}")
        return "Erro"
    
def get_tiktok_followers():
    url = "https://instagram-statistics-api.p.rapidapi.com/community"
    querystring = {"url": f"https://www.tiktok.com/@{TIKTOK_USER}"}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "instagram-statistics-api.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        data = response.json()
        
        # Acessa o número de seguidores
        followers = data["data"]["usersCount"]
        return followers
    except Exception as e:
        print(f"Erro na requisição do TikTok: {e}")
        return "Erro"


# Comando do bot para exibir seguidores
@bot.command()
async def seguidores(ctx):
    instagram = get_instagram_followers()
    youtube = get_youtube_followers()
    tiktok = get_tiktok_followers()
    
    embed = discord.Embed(title="📊 Seguidores de @joaoluzx", color=0x00ff00)
    embed.add_field(name="Instagram", value=f"📸 {instagram} seguidores", inline=False)
    embed.add_field(name="YouTube", value=f"▶️ {youtube} inscritos", inline=False)
    embed.add_field(name="TikTok", value=f"🎵 {tiktok} seguidores", inline=False)
    
    await ctx.send(embed=embed)


# Rodar o bot
bot.run(TOKEN)