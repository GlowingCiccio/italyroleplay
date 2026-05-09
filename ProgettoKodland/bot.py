import discord
from discord import app_commands
import httpx

BOT_TOKEN   = "MTUwMjYwMDQzMTk4ODM3OTY3OQ.GE3C1m.mgZbVK1GxAvuwKLQN4mSgIgsRIEqZSITUYeXr4"
BOT_SECRET  = "kodland"
BACKEND_URL = "http://127.0.0.1:8000"

intents = discord.Intents.default()
client  = discord.Client(intents=intents)
tree    = app_commands.CommandTree(client)


async def call_backend(user_id: int, action: str):
    async with httpx.AsyncClient() as http:
        res = await http.post(
            f"{BACKEND_URL}/set-premium",
            json={"user_id": str(user_id), "action": action},
            headers={"X-Bot-Secret": BOT_SECRET},
        )
    return res.json()


@tree.command(name="premium", description="Attiva il premium per un utente")
@app_commands.checks.has_permissions(administrator=True)
async def cmd_premium(interaction: discord.Interaction, utente: discord.Member):
    await call_backend(utente.id, "add")
    embed = discord.Embed(
        title="Premium attivato",
        description=f"{utente.mention} è ora PREMIUM.",
        color=0xF5C400,
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="nopremium", description="Rimuove il premium da un utente")
@app_commands.checks.has_permissions(administrator=True)
async def cmd_nopremium(interaction: discord.Interaction, utente: discord.Member):
    await call_backend(utente.id, "remove")
    embed = discord.Embed(
        title="Premium rimosso",
        description=f"{utente.mention} è tornato FREE.",
        color=0x5865F2,
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@cmd_premium.error
@cmd_nopremium.error
async def perm_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("Solo gli amministratori possono usare questo comando.", ephemeral=True)


# ─── SETUP ────────────────────────────────────────────────────

RUOLI = [
    {"name": "🛡️ ADMIN",      "color": discord.Color.red(),    "hoist": True, "permissions": discord.Permissions.all()},
    {"name": "🔨 Moderatore", "color": discord.Color.orange(), "hoist": True, "permissions": discord.Permissions(moderate_members=True, manage_messages=True)},
    {"name": "👶 Membro",     "color": discord.Color.blue(),   "hoist": True, "permissions": discord.Permissions.general()},
]

STRUTTURA = {
    "📢 INFORMAZIONI": ["📌regole", "📣annunci", "🎉benvenuto"],
    "💬 GENERALE":     ["💬chat-generale", "🎮gaming", "🖼️media"],
    "🔧 STAFF":        ["📋staff-chat", "📝log-moderazione", "🤖comandi"],
}

CANALI_VOCALI = {
    "🔊 VOICE": ["Generale", "Gaming", "AFK"],
}

@tree.command(name="setup", description="Configura automaticamente ruoli e canali del server")
@app_commands.checks.has_permissions(administrator=True)
async def setup(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    log = []

    ruoli_creati = {}
    for dati in RUOLI:
        esistente = discord.utils.get(guild.roles, name=dati["name"])
        if esistente:
            ruoli_creati[dati["name"]] = esistente
            log.append(f"⚠️ Ruolo **{dati['name']}** già esistente, saltato")
            continue
        ruolo = await guild.create_role(
            name=dati["name"], color=dati["color"],
            hoist=dati["hoist"], permissions=dati["permissions"],
            reason="Setup automatico"
        )
        ruoli_creati[dati["name"]] = ruolo
        log.append(f"✅ Ruolo {ruolo.mention} creato")

    ruolo_staff = ruoli_creati.get("Moderatore")

    for nome_categoria, canali in STRUTTURA.items():
        overwrites = {guild.default_role: discord.PermissionOverwrite(view_channel=True, send_messages=True)}
        if "STAFF" in nome_categoria and ruolo_staff:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                ruolo_staff: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            }
        categoria = await guild.create_category(nome_categoria, overwrites=overwrites)
        log.append(f"📁 **{nome_categoria}**")
        for nome_canale in canali:
            await categoria.create_text_channel(nome_canale)
            log.append(f"  └ #{nome_canale}")

    for nome_categoria, canali in CANALI_VOCALI.items():
        categoria = await guild.create_category(nome_categoria)
        for nome_canale in canali:
            await categoria.create_voice_channel(nome_canale)
            log.append(f"  └ 🔊 {nome_canale}")

    embed = discord.Embed(title="✅ Setup completato!", description="\n".join(log), color=discord.Color.green())
    embed.set_footer(text=f"Eseguito da {interaction.user}")
    await interaction.followup.send(embed=embed, ephemeral=True)

@setup.error
async def setup_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ Devi essere amministratore!", ephemeral=True)

# ──────────────────────────────────────────────────────────────


@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot online come {client.user}")


client.run(BOT_TOKEN)