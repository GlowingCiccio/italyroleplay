import discord
from discord import app_commands
import datetime
import json
import os

# ─────────────────────────────────────────────
#  CONFIGURAZIONE — sostituisci con i tuoi dati
# ─────────────────────────────────────────────
BOT_TOKEN      = "INSERISCI"
GUILD_ID       = int("INSERISCI")
ROLE_MEMBRO_ID = int("INSERISCI")
ROLE_STAFF_ID  = int("INSERISCI")
ROLE_ADMIN_ID  = int("INSERISCI")
ROLE_PREMIUM_ID = int("INSERISCI")  
WELCOME_CH_ID  = int("INSERISCI")
LOG_CH_ID      = int("INSERISCI")
RULES_CH_ID    = int("INSERISCI")
TICKET_CH_ID   = int("INSERISCI")
# ─────────────────────────────────────────────

WARNS_FILE = "warns.json"

# ════════════════════════════════════════════════
#  CLIENT
# ════════════════════════════════════════════════

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class ItalyRP(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print(f"✅ Slash commands sincronizzati sul guild {GUILD_ID}")

bot = ItalyRP()
GUILD = discord.Object(id=GUILD_ID)

# ════════════════════════════════════════════════
#  UTILITY
# ════════════════════════════════════════════════

def load_warns() -> dict:
    if os.path.exists(WARNS_FILE):
        with open(WARNS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_warns(data: dict):
    with open(WARNS_FILE, "w") as f:
        json.dump(data, f, indent=2)

async def send_log(guild: discord.Guild, embed: discord.Embed):
    ch = guild.get_channel(LOG_CH_ID)
    if ch:
        await ch.send(embed=embed)

def is_staff(interaction: discord.Interaction) -> bool:
    staff = interaction.guild.get_role(ROLE_STAFF_ID)
    admin = interaction.guild.get_role(ROLE_ADMIN_ID)
    return (staff and staff in interaction.user.roles) or \
           (admin and admin in interaction.user.roles) or \
           interaction.user.guild_permissions.administrator

def is_admin(interaction: discord.Interaction) -> bool:
    admin = interaction.guild.get_role(ROLE_ADMIN_ID)
    return (admin and admin in interaction.user.roles) or \
           interaction.user.guild_permissions.administrator

# ════════════════════════════════════════════════
#  EVENTS
# ════════════════════════════════════════════════

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"🔄 Comandi sincronizzati: {len(synced)}")
    except Exception as e:
        print(f"Errore sync: {e}")

    print(f"✅ Bot online come {bot.user}")

@bot.event
async def on_member_join(member: discord.Member):
    role = member.guild.get_role(ROLE_MEMBRO_ID)
    if role:
        await member.add_roles(role, reason="Auto-join")

    ch = member.guild.get_channel(WELCOME_CH_ID)
    if ch:
        embed = discord.Embed(
            title="🇮🇹 Benvenuto in Italy RP!",
            description=(
                f"Ciao {member.mention}! Sei il membro numero **{member.guild.member_count}**.\n\n"
                f"📋 Leggi le regole in <#{RULES_CH_ID}>\n"
                f"🎫 Apri un ticket in <#{TICKET_CH_ID}> per qualsiasi dubbio\n"
                f"🎮 Buon roleplay!"
            ),
            color=0x5c6ef5,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Italy RP • Portal System")
        await ch.send(embed=embed)

    log = discord.Embed(
        title="📥 Nuovo membro",
        description=f"{member.mention} (`{member.id}`) è entrato nel server.",
        color=0x3ddc84,
        timestamp=datetime.datetime.utcnow()
    )
    log.set_thumbnail(url=member.display_avatar.url)
    await send_log(member.guild, log)

@bot.event
async def on_member_remove(member: discord.Member):
    log = discord.Embed(
        title="📤 Membro uscito",
        description=f"**{member}** (`{member.id}`) ha lasciato il server.",
        color=0xf55c5c,
        timestamp=datetime.datetime.utcnow()
    )
    await send_log(member.guild, log)

# ════════════════════════════════════════════════
#  SLASH — GENERALI
# ════════════════════════════════════════════════

@bot.tree.command(name="ping", description="Mostra la latenza del bot", guild=GUILD)
async def cmd_ping(interaction: discord.Interaction):
    ms = round(bot.latency * 1000)
    color = 0x3ddc84 if ms < 100 else 0xf39c12 if ms < 200 else 0xf55c5c
    embed = discord.Embed(title="🏓 Pong!", color=color)
    embed.add_field(name="Latenza", value=f"`{ms}ms`")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="info", description="Mostra le informazioni del server", guild=GUILD)
async def cmd_info(interaction: discord.Interaction):
    g = interaction.guild
    embed = discord.Embed(title=f"📊 {g.name}", color=0x5c6ef5, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="👥 Membri", value=g.member_count)
    embed.add_field(name="🏷️ Ruoli", value=len(g.roles))
    embed.add_field(name="💬 Canali", value=len(g.channels))
    embed.add_field(name="📅 Creato il", value=g.created_at.strftime("%d/%m/%Y"))
    embed.add_field(name="🌍 Lingua", value="Italiano 🇮🇹")
    embed.add_field(name="🎮 Framework", value="ESX — FiveM")
    if g.icon:
        embed.set_thumbnail(url=g.icon.url)
    embed.set_footer(text="Italy RP Portal")
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="profilo", description="Mostra il tuo profilo nel server", guild=GUILD)
async def cmd_profilo(interaction: discord.Interaction):
    m = interaction.user
    roles = [r.mention for r in m.roles if r.name != "@everyone"]
    warns = load_warns()
    n_warns = len(warns.get(str(m.id), []))
    embed = discord.Embed(title=f"👤 {m.display_name}", color=0x5c6ef5, timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=m.display_avatar.url)
    embed.add_field(name="🏷️ Tag", value=str(m))
    embed.add_field(name="🆔 ID", value=f"`{m.id}`")
    embed.add_field(name="📅 Nel server dal", value=m.joined_at.strftime("%d/%m/%Y") if m.joined_at else "N/A")
    embed.add_field(name="📆 Account creato", value=m.created_at.strftime("%d/%m/%Y"))
    embed.add_field(name="⚠️ Warns", value=f"{n_warns}/3")
    embed.add_field(name="🎭 Ruoli", value=" ".join(roles) if roles else "Nessuno", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="regole", description="Mostra il regolamento del server", guild=GUILD)
async def cmd_regole(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📋 Regolamento Italy RP",
        color=0x5c6ef5,
        description=(
            "**§1 — Comportamento**\n"
            "> `1.` Rispetta tutti i giocatori, sempre.\n"
            "> `2.` Parla in italiano in gioco.\n\n"
            "**§2 — Roleplay**\n"
            "> `3.` No **Metagaming** — niente info OOC in gioco.\n"
            "> `4.` No **Powergaming** — non forzare azioni su altri.\n"
            "> `5.` **NLR** — dopo la morte dimentica tutto, aspetta 15 min.\n"
            "> `6.` **Valore della vita** — comportati come se tenessi a vivere.\n\n"
            "**§3 — Combattimento**\n"
            "> `7.` No **RDM** — uccidere senza motivo RP è vietato.\n"
            "> `8.` No **VDM** — investire con veicoli è vietato.\n\n"
            "**§4 — Tecnico**\n"
            "> `9.` No cheat, trainer o exploit. **Ban permanente.**\n"
            "> `10.` Rispetta le decisioni dello staff."
        ),
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_footer(text=f"Italy RP • Regole complete in <#{RULES_CH_ID}>")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="miei_warns", description="Visualizza i tuoi warn", guild=GUILD)
async def cmd_miei_warns(interaction: discord.Interaction):
    warns = load_warns()
    user_warns = warns.get(str(interaction.user.id), [])
    if not user_warns:
        await interaction.response.send_message("✅ Non hai nessun warn!", ephemeral=True)
        return
    embed = discord.Embed(title=f"⚠️ I tuoi warn ({len(user_warns)}/3)", color=0xf39c12)
    for i, w in enumerate(user_warns, 1):
        embed.add_field(name=f"Warn #{i} — {w['data']}", value=f"**Motivo:** {w['motivo']}\n**Staff:** {w['staff']}", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="ticket", description="Info su come aprire un ticket con lo staff", guild=GUILD)
async def cmd_ticket(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎫 Apri un Ticket",
        description=(
            f"Vai in <#{TICKET_CH_ID}> e segui le istruzioni.\n\n"
            "Puoi aprire un ticket per:\n"
            "• 🐛 Segnalare un bug\n"
            "• ⚠️ Segnalare un giocatore\n"
            "• 🤝 Candidarti allo staff\n"
            "• ❓ Dubbi sulle regole"
        ),
        color=0x5c6ef5
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


# ════════════════════════════════════════════════
#  SLASH — STAFF
# ════════════════════════════════════════════════

@bot.tree.command(name="warn", description="[STAFF] Assegna un warn a un membro", guild=GUILD)
@app_commands.describe(membro="Il membro da warnare", motivo="Motivo del warn")
async def cmd_warn(interaction: discord.Interaction, membro: discord.Member, motivo: str = "Nessun motivo specificato"):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Non hai i permessi.", ephemeral=True)
        return

    warns = load_warns()
    uid = str(membro.id)
    if uid not in warns:
        warns[uid] = []
    warns[uid].append({
        "motivo": motivo,
        "staff": str(interaction.user),
        "data": datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M")
    })
    save_warns(warns)
    total = len(warns[uid])

    embed = discord.Embed(title="⚠️ Warn Assegnato", color=0xf39c12, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Utente", value=membro.mention)
    embed.add_field(name="Staff", value=interaction.user.mention)
    embed.add_field(name="Motivo", value=motivo, inline=False)
    embed.add_field(name="Warn totali", value=f"{total}/3")
    embed.set_thumbnail(url=membro.display_avatar.url)
    await interaction.response.send_message(embed=embed)

    try:
        dm = discord.Embed(title="⚠️ Hai ricevuto un warn su Italy RP", description=f"**Motivo:** {motivo}\n**Warn totali:** {total}/3\n\nSe ritieni il warn ingiusto apri un ticket.", color=0xf39c12)
        await membro.send(embed=dm)
    except discord.Forbidden:
        pass

    await send_log(interaction.guild, embed)

    if total >= 3:
        try:
            await membro.kick(reason="3 warn — kick automatico")
            ke = discord.Embed(title="👢 Kick Automatico (3 warn)", description=f"{membro.mention} kickato automaticamente.", color=0xe74c3c, timestamp=datetime.datetime.utcnow())
            await send_log(interaction.guild, ke)
        except discord.Forbidden:
            pass


@bot.tree.command(name="warn_lista", description="[STAFF] Visualizza i warn di un membro", guild=GUILD)
@app_commands.describe(membro="Il membro di cui vedere i warn")
async def cmd_warn_lista(interaction: discord.Interaction, membro: discord.Member):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Non hai i permessi.", ephemeral=True)
        return
    warns = load_warns()
    user_warns = warns.get(str(membro.id), [])
    if not user_warns:
        await interaction.response.send_message(f"✅ {membro.mention} non ha warn.", ephemeral=True)
        return
    embed = discord.Embed(title=f"⚠️ Warn di {membro} ({len(user_warns)}/3)", color=0xf39c12)
    for i, w in enumerate(user_warns, 1):
        embed.add_field(name=f"#{i} — {w['data']}", value=f"**Motivo:** {w['motivo']}\n**Staff:** {w['staff']}", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="warn_rimuovi", description="[STAFF] Rimuove l'ultimo warn di un membro", guild=GUILD)
@app_commands.describe(membro="Il membro a cui rimuovere il warn")
async def cmd_warn_rimuovi(interaction: discord.Interaction, membro: discord.Member):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Non hai i permessi.", ephemeral=True)
        return
    warns = load_warns()
    uid = str(membro.id)
    if not warns.get(uid):
        await interaction.response.send_message(f"✅ {membro.mention} non ha warn.", ephemeral=True)
        return
    warns[uid].pop()
    save_warns(warns)
    await interaction.response.send_message(f"✅ Rimosso l'ultimo warn di {membro.mention}. Rimasti: **{len(warns[uid])}/3**.", ephemeral=True)


@bot.tree.command(name="kick", description="[STAFF] Espelle un membro dal server", guild=GUILD)
@app_commands.describe(membro="Il membro da kickare", motivo="Motivo del kick")
async def cmd_kick(interaction: discord.Interaction, membro: discord.Member, motivo: str = "Nessun motivo specificato"):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Non hai i permessi.", ephemeral=True)
        return
    if membro.top_role >= interaction.user.top_role:
        await interaction.response.send_message("❌ Non puoi kickare un membro con ruolo uguale o superiore al tuo.", ephemeral=True)
        return
    try:
        await membro.send(embed=discord.Embed(title="👢 Sei stato espulso da Italy RP", description=f"**Motivo:** {motivo}", color=0xe74c3c))
    except discord.Forbidden:
        pass
    await membro.kick(reason=motivo)
    embed = discord.Embed(title="👢 Membro Kickato", color=0xe74c3c, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Utente", value=str(membro))
    embed.add_field(name="Staff", value=interaction.user.mention)
    embed.add_field(name="Motivo", value=motivo, inline=False)
    await interaction.response.send_message(embed=embed)
    await send_log(interaction.guild, embed)


@bot.tree.command(name="ban", description="[STAFF] Banna un membro dal server", guild=GUILD)
@app_commands.describe(membro="Il membro da bannare", motivo="Motivo del ban", giorni_messaggi="Giorni di messaggi da cancellare (0-7)")
async def cmd_ban(interaction: discord.Interaction, membro: discord.Member, motivo: str = "Nessun motivo specificato", giorni_messaggi: int = 0):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Non hai i permessi.", ephemeral=True)
        return
    if membro.top_role >= interaction.user.top_role:
        await interaction.response.send_message("❌ Non puoi bannare un membro con ruolo uguale o superiore al tuo.", ephemeral=True)
        return
    try:
        await membro.send(embed=discord.Embed(title="🔨 Sei stato bannato da Italy RP", description=f"**Motivo:** {motivo}", color=0xc0392b))
    except discord.Forbidden:
        pass
    await membro.ban(reason=motivo, delete_message_days=max(0, min(7, giorni_messaggi)))
    embed = discord.Embed(title="🔨 Membro Bannato", color=0xc0392b, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Utente", value=str(membro))
    embed.add_field(name="Staff", value=interaction.user.mention)
    embed.add_field(name="Motivo", value=motivo, inline=False)
    await interaction.response.send_message(embed=embed)
    await send_log(interaction.guild, embed)


@bot.tree.command(name="unban", description="[ADMIN] Rimuove il ban di un utente tramite ID", guild=GUILD)
@app_commands.describe(user_id="ID Discord dell'utente", motivo="Motivo dell'unban")
async def cmd_unban(interaction: discord.Interaction, user_id: str, motivo: str = "Nessun motivo specificato"):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ Solo gli admin possono sbannare.", ephemeral=True)
        return
    try:
        user = await bot.fetch_user(int(user_id))
        await interaction.guild.unban(user, reason=motivo)
        embed = discord.Embed(title="✅ Utente Sbannato", color=0x3ddc84, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Utente", value=f"{user} (`{user.id}`)")
        embed.add_field(name="Admin", value=interaction.user.mention)
        embed.add_field(name="Motivo", value=motivo, inline=False)
        await interaction.response.send_message(embed=embed)
        await send_log(interaction.guild, embed)
    except (ValueError, discord.NotFound):
        await interaction.response.send_message("❌ ID non valido o utente non in lista ban.", ephemeral=True)


@bot.tree.command(name="muto", description="[STAFF] Mette in timeout un membro", guild=GUILD)
@app_commands.describe(membro="Il membro", minuti="Durata in minuti", motivo="Motivo")
async def cmd_muto(interaction: discord.Interaction, membro: discord.Member, minuti: int, motivo: str = "Nessun motivo specificato"):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Non hai i permessi.", ephemeral=True)
        return
    durata = datetime.timedelta(minutes=max(1, min(40320, minuti)))
    await membro.timeout(datetime.datetime.utcnow() + durata, reason=motivo)
    embed = discord.Embed(title="🔇 Membro Mutato", color=0xf39c12, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Utente", value=membro.mention)
    embed.add_field(name="Durata", value=f"{minuti} min")
    embed.add_field(name="Staff", value=interaction.user.mention)
    embed.add_field(name="Motivo", value=motivo, inline=False)
    await interaction.response.send_message(embed=embed)
    await send_log(interaction.guild, embed)


@bot.tree.command(name="smuto", description="[STAFF] Rimuove il timeout da un membro", guild=GUILD)
@app_commands.describe(membro="Il membro da smutare")
async def cmd_smuto(interaction: discord.Interaction, membro: discord.Member):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Non hai i permessi.", ephemeral=True)
        return
    await membro.timeout(None)
    await interaction.response.send_message(f"🔊 Timeout rimosso per {membro.mention}.", ephemeral=True)


@bot.tree.command(name="purge", description="[STAFF] Elimina messaggi dal canale corrente", guild=GUILD)
@app_commands.describe(quantita="Numero di messaggi da eliminare (1-100)")
async def cmd_purge(interaction: discord.Interaction, quantita: int):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Non hai i permessi.", ephemeral=True)
        return
    if not 1 <= quantita <= 100:
        await interaction.response.send_message("❌ Valore tra 1 e 100.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=quantita)
    await interaction.followup.send(f"🗑️ Eliminati **{len(deleted)}** messaggi.", ephemeral=True)
    log = discord.Embed(title="🗑️ Purge", color=0xf39c12, timestamp=datetime.datetime.utcnow())
    log.add_field(name="Canale", value=interaction.channel.mention)
    log.add_field(name="Staff", value=interaction.user.mention)
    log.add_field(name="Eliminati", value=str(len(deleted)))
    await send_log(interaction.guild, log)


@bot.tree.command(name="ruolo_dai", description="[STAFF] Assegna un ruolo a un membro", guild=GUILD)
@app_commands.describe(membro="Il membro", ruolo="Il ruolo da assegnare")
async def cmd_ruolo_dai(interaction: discord.Interaction, membro: discord.Member, ruolo: discord.Role):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Non hai i permessi.", ephemeral=True)
        return
    await membro.add_roles(ruolo)
    await interaction.response.send_message(f"✅ **{ruolo.name}** assegnato a {membro.mention}.", ephemeral=True)
    log = discord.Embed(title="🏷️ Ruolo Assegnato", color=0x3ddc84, timestamp=datetime.datetime.utcnow())
    log.add_field(name="Utente", value=membro.mention)
    log.add_field(name="Ruolo", value=ruolo.mention)
    log.add_field(name="Staff", value=interaction.user.mention)
    await send_log(interaction.guild, log)


@bot.tree.command(name="ruolo_togli", description="[STAFF] Rimuove un ruolo da un membro", guild=GUILD)
@app_commands.describe(membro="Il membro", ruolo="Il ruolo da rimuovere")
async def cmd_ruolo_togli(interaction: discord.Interaction, membro: discord.Member, ruolo: discord.Role):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Non hai i permessi.", ephemeral=True)
        return
    await membro.remove_roles(ruolo)
    await interaction.response.send_message(f"✅ **{ruolo.name}** rimosso da {membro.mention}.", ephemeral=True)


@bot.tree.command(name="slowmode", description="[STAFF] Imposta lo slowmode nel canale corrente", guild=GUILD)
@app_commands.describe(secondi="Secondi di slowmode (0 = disabilita)")
async def cmd_slowmode(interaction: discord.Interaction, secondi: int):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Non hai i permessi.", ephemeral=True)
        return
    await interaction.channel.edit(slowmode_delay=max(0, secondi))
    msg = "✅ Slowmode disabilitato." if secondi == 0 else f"✅ Slowmode impostato a **{secondi}s**."
    await interaction.response.send_message(msg, ephemeral=True)


@bot.tree.command(name="annuncio", description="[ADMIN] Invia un annuncio embed in un canale", guild=GUILD)
@app_commands.describe(canale="Canale di destinazione", titolo="Titolo dell'annuncio", testo="Testo dell'annuncio")
async def cmd_annuncio(interaction: discord.Interaction, canale: discord.TextChannel, titolo: str, testo: str):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ Solo gli admin possono inviare annunci.", ephemeral=True)
        return
    embed = discord.Embed(title=f"📢 {titolo}", description=testo, color=0x5c6ef5, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"Italy RP — {interaction.user.display_name}")
    await canale.send("@everyone", embed=embed)
    await interaction.response.send_message(f"✅ Annuncio inviato in {canale.mention}.", ephemeral=True)


# ════════════════════════════════════════════════
#  PREMIUM
# ════════════════════════════════════════════════

@bot.tree.command(name="premium", description="[STAFF] Assegna il premium a un utente", guild=GUILD)
@app_commands.describe(membro="Il membro a cui dare il premium")
async def cmd_premium(interaction: discord.Interaction, membro: discord.Member):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Non hai i permessi.", ephemeral=True)
        return

    ruolo = interaction.guild.get_role(ROLE_PREMIUM_ID)
    if not ruolo:
        await interaction.response.send_message("❌ Ruolo premium non trovato.", ephemeral=True)
        return

    await membro.add_roles(ruolo)
    await interaction.response.send_message(f"🌟 Premium assegnato a {membro.mention}!", ephemeral=True)

    log = discord.Embed(
        title="🌟 Premium Assegnato",
        description=f"{membro.mention} ha ricevuto il ruolo premium.",
        color=0xf1c40f,
        timestamp=datetime.datetime.utcnow()
    )
    await send_log(interaction.guild, log)


@bot.tree.command(name="leva_premium", description="[STAFF] Rimuove il premium da un utente", guild=GUILD)
@app_commands.describe(membro="Il membro a cui togliere il premium")
async def cmd_leva_premium(interaction: discord.Interaction, membro: discord.Member):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Non hai i permessi.", ephemeral=True)
        return

    ruolo = interaction.guild.get_role(ROLE_PREMIUM_ID)
    if not ruolo:
        await interaction.response.send_message("❌ Ruolo premium non trovato.", ephemeral=True)
        return

    await membro.remove_roles(ruolo)
    await interaction.response.send_message(f"🗑️ Premium rimosso da {membro.mention}.", ephemeral=True)

    log = discord.Embed(
        title="🗑️ Premium Rimosso",
        description=f"{membro.mention} non è più premium.",
        color=0xe74c3c,
        timestamp=datetime.datetime.utcnow()
    )
    await send_log(interaction.guild, log)


# ════════════════════════════════════════════════
bot.run(BOT_TOKEN)
