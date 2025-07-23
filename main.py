import discord
from discord import app_commands
import json
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)
token = os.getenv("TOKEN")
RANKING_FILE = "ranking.json"
DEV_GUILD_ID = None  

intents = discord.Intents.default()

class MeuBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        if DEV_GUILD_ID:
            guild = discord.Object(id=DEV_GUILD_ID)
            await self.tree.sync(guild=guild)
            print("🔧 Comandos sincronizados no servidor de teste.")
        else:
            await self.tree.sync()
            print("🌍 Comandos globais sincronizados.")
        print(f'✅ Bot conectado como {self.user}')

bot = MeuBot()

# Utils
def carregar_ranking():
    if not os.path.exists(RANKING_FILE):
        with open(RANKING_FILE, "w") as f:
            json.dump({}, f)

    with open(RANKING_FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return {}
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {}

def salvar_ranking(ranking):
    with open(RANKING_FILE, "w") as f:
        json.dump(ranking, f, indent=4)

def registrar_ataque(user: discord.Member, tipo: str):
    ranking = carregar_ranking()
    user_id = str(user.id)

    if user_id not in ranking:
        ranking[user_id] = {
            "username": user.display_name,
            "petecos recebidos": 0,
            "bandecadas recebidas": 0,
            "caronas recebidas": 0,
            "levados para bananeira": 0,
            "calcinhas usadas": 0,
            "pedras jogadas": 0
        }

    ranking[user_id][tipo] += 1
    salvar_ranking(ranking)

# Comandos
@bot.tree.command(name="bandecar", description="Você bandeca um usuário")
@app_commands.describe(usuario="Usuário a ser bandecado")
async def bandecar(interaction: discord.Interaction, usuario: discord.Member):
    registrar_ataque(usuario, "bandecadas recebidas")
    await interaction.response.send_message(f'{interaction.user.mention} bandecou {usuario.mention}')

@bot.tree.command(name="prarir", description="Mostra uma mensagem divertida")
async def prarir(interaction: discord.Interaction):
    await interaction.response.send_message('Se é pra rir tá tudo bem')

@bot.tree.command(name="isher", description="Pare de qualiragens")
async def isher(interaction: discord.Interaction):
    await interaction.response.send_message('IIISHEEEEEEEEEEERRRRRRRR🏳️‍🌈')

@bot.tree.command(name="carona", description="Leva alguém a algum lugar 😈")
@app_commands.describe(usuario="Usuário que vai receber a carona")
async def carona(interaction: discord.Interaction, usuario: discord.Member):
    registrar_ataque(usuario, "caronas recebidas")
    with open("imgs\carona.gif", "rb") as gif:
        await interaction.response.send_message(
            f'{interaction.user.mention} deu uma carona pra {usuario.mention}', file=discord.File(gif)
        )

@bot.tree.command(name="peteco", description="Dá petecos virtuais em alguém")
@app_commands.describe(usuario="Usuário que vai levar peteco")
async def peteco(interaction: discord.Interaction, usuario: discord.Member):
    registrar_ataque(usuario, "petecos recebidos")
    with open("imgs\peteco.png", "rb") as img:
        await interaction.response.send_message(
            f'{interaction.user.mention} deu petecos virtuais em {usuario.mention}', file=discord.File(img)
        )

@bot.tree.command(name="bananeira", description="Leva alguém pra atrás da bananeira")
@app_commands.describe(usuario="Usuário que vai levar pra bananeira")
async def bananeira(interaction: discord.Interaction, usuario: discord.Member):
    registrar_ataque(usuario, "levados para bananeira")
    with open("imgs\bananeira.gif", "rb") as gif:
        await interaction.response.send_message(
            f'{interaction.user.mention} levou {usuario.mention} para atrás da bananeira', file=discord.File(gif)
        )

@bot.tree.command(name="montesinai", description="Mais uma pizza feita na Monte Sinai")
async def montesinai(interaction: discord.Interaction):
    with open("imgs\pizza.gif", "rb") as gif:
        await interaction.response.send_message("Mais uma pizza sendo feita na Monte Sinai 🍕", file=discord.File(gif))

@bot.tree.command(name="cambio", description="Rapaz...")
async def cambio(interaction: discord.Interaction):
    with open("imgs\desligo.gif", "rb") as gif:
        await interaction.response.send_message("Rapaz... oia é o seguinte... rapa.. rum... Câmbio desligo!", file=discord.File(gif))

@bot.tree.command(name="alo", description="testando")
async def alo(interaction: discord.Interaction):
    with open("imgs\alosom.gif", "rb") as gif:
        await interaction.response.send_message("Alô som", file=discord.File(gif))

@bot.tree.command(name="pizzaiolo", description="Olha a habilidade")
async def pizzaiolo(interaction: discord.Interaction):
    with open("imgs\pizzaiolo.gif", "rb") as gif:
        await interaction.response.send_message("Olha a habilidade dos pizzaiolos da Monte Sinai!!", file=discord.File(gif))

@bot.tree.command(name="pedra", description="Taca pedra na cabeça de alguém")
@app_commands.describe(usuario="Usuário que vai levar a pedrada")
async def pedra(interaction: discord.Interaction, usuario: discord.Member):
    registrar_ataque(usuario, "pedras jogadas")
    with open("imgs\pedra.gif", "rb") as gif:
        await interaction.response.send_message(
            f'{interaction.user.mention} tacou a pedra em {usuario.mention}', file=discord.File(gif)
        )

@bot.tree.command(name="calcinha", description="...")
async def calcinha(interaction: discord.Interaction):
    registrar_ataque(interaction.user, "calcinhas usadas")  # corrigido
    with open("imgs\calcinha.png", "rb") as img:
        await interaction.response.send_message(f'{interaction.user.mention} usou calcinha', file=discord.File(img))

@bot.tree.command(name="time", description="Mostra o melhor time")
async def time(interaction: discord.Interaction):
    await interaction.response.send_message("Não tem jeito, o melhor time é João Henrique, Guilherme, Alan e Laura!!!!")

@bot.tree.command(name="ranking", description="Exibe o ranking de petecos e bandecadas")
async def ranking(interaction: discord.Interaction):
    ranking = carregar_ranking()
    if not ranking:
        await interaction.response.send_message("Ninguém foi bandecado ainda! 👼")
        return

    ordenado = sorted(
        ranking.items(),
        key=lambda x: x[1]["petecos recebidos"] + x[1]["bandecadas recebidas"],
        reverse=True
    )

    embed = discord.Embed(title="🏆 Ranking de Bandecadas Virtuais", color=discord.Color.gold())

    for i, (user_id, data) in enumerate(ordenado, 1):
        embed.add_field(
            name=f"{i}. {data['username']}",
            value=(
                f"👋 Petecos recebidos: {data['petecos recebidos']} | "
                f"😡 Bandecadas recebidas: {data['bandecadas recebidas']} | "
                f"🚗 Caronas recebidas: {data['caronas recebidas']} | "
                f"🌴 Levados para a bananeira: {data['levados para bananeira']} | "
                f"🩲 Calcinhas usadas: {data['calcinhas usadas']} | "
                f"🪨 Pedras jogadas: {data['pedras jogadas']}"
            ),
            inline=False
        )

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="Mostra todos os comandos disponíveis")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Comandos disponíveis 🤖",
        description="Aqui estão os comandos que você pode usar:",
        color=discord.Color.blue()
    )
    comandos = [
        ("/bandecar @usuário", "Você bandeca alguém 😠"),
        ("/prarir", "Se é pra rir... 😄"),
        ("/isher", "Pare de qualiragens"),
        ("/montesinai", "Uma pizza será feita 🍕"),
        ("/peteco @usuário", "Dá petecos virtuais 👋"),
        ("/carona @usuário", "Leva alguém de carona 🚗"),
        ("/ranking", "Exibe o ranking de bandecadas 🏆"),
        ("/time", "O melhor time do planeta 💪"),
        ("/alo", "Alô som 🎤"),
        ("/cambio", "Câmbio, desligo 📻"),
        ("/bananeira @usuário", "Leva alguém para trás da bananeira 🌴"),
        ("/calcinha", "Cheira uma ...."),
    ]

    for nome, desc in comandos:
        embed.add_field(name=nome, value=desc, inline=False)

    await interaction.response.send_message(embed=embed)

# Executar o bot
bot.run(token)
