<div align="center">
  
  <img src="https://cdn.discordapp.com/icons/1431571702747238463/your_server_icon.png" width="150" style="border-radius: 50%;">
  
  # 🇮🇹 Italy RP Portal – Installazione
  
  ### Sistema completo di gestione Discord + Portale Web Premium
  
  [![Discord](https://img.shields.io/badge/Discord-Join-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/ZQBGEnfMfC)
  [![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
  [![Discord.py](https://img.shields.io/badge/Discord.py-2.3+-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io)
  
  <p align="center">
    <strong>✨ Guida ufficiale per installare e configurare Italy RP Portal ✨</strong>
  </p>

</div>

---

# 📌 Passo 1 – Crea l'app Discord

1. Vai su **https://discord.com/developers/applications**
2. Clicca **New Application**
3. Nome: `Italy RP Portal` → **Create**
4. Menu sinistro → **Bot** → **Add Bot**
5. Clicca **Reset Token** → **COPIA IL TOKEN**
6. Attiva:
   - `SERVER MEMBERS INTENT`
   - `MESSAGE CONTENT INTENT`
7. Menu sinistro → **OAuth2** → **General**
8. In **Redirects** aggiungi:
   ```
   http://localhost:8000/callback
   ```
9. Copia e salva:
   - **Client ID**
   - **Client Secret**

---

# 📌 Passo 2 – Prendi gli ID dal server

### 🔧 Attiva modalità sviluppatore

- Discord → Impostazioni → **Avanzate** → Modalità sviluppatore → **ON**

### 📌 Copia questi ID

| Cosa | Come fare |
|------|-----------|
| 🏛️ ID Server | Tasto destro sul nome del server |
| 👤 ID Ruolo Membro | Tasto destro sul ruolo |
| 🛡️ ID Ruolo Staff | Tasto destro sul ruolo |
| 👑 ID Ruolo Admin | Tasto destro sul ruolo |
| 💎 ID Ruolo Premium | Tasto destro sul ruolo |
| 👋 ID Canale Benvenuto | Tasto destro sul canale |
| 📁 ID Canale Log | Tasto destro sul canale |
| 📜 ID Canale Regole | Tasto destro sul canale |
| 🎫 ID Canale Ticket | Tasto destro sul canale |

---

# 📌 Passo 3 – Configura `bot.py`

Modifica queste righe:

```python
BOT_TOKEN = "incolla_il_tuo_token_qui"

GUILD_ID        = 123456789012345678
ROLE_MEMBRO_ID  = 123456789012345678
ROLE_STAFF_ID   = 123456789012345678
ROLE_ADMIN_ID   = 123456789012345678
ROLE_PREMIUM_ID = 123456789012345678

WELCOME_CH_ID   = 123456789012345678
LOG_CH_ID       = 123456789012345678
RULES_CH_ID     = 123456789012345678
TICKET_CH_ID    = 123456789012345678
```

> ⚠️ **IMPORTANTE:** qui gli ID vanno **SENZA virgolette**.

---

# 📌 Passo 4 – Configura `server.py`

```python
CLIENT_ID     = "incolla_il_tuo_client_id_qui"
CLIENT_SECRET = "incolla_il_tuo_client_secret_qui"

BOT_TOKEN = "incolla_il_tuo_token_qui"

GUILD_ID        = "id_del_tuo_server_qui"
ROLE_PREMIUM_ID = "id_ruolo_premium_qui"
```

> ⚠️ **IMPORTANTE:** qui gli ID vanno **CON le virgolette**.

---

# 📌 Passo 5 – Installa le dipendenze

Apri il terminale e incolla:

```bash
pip install fastapi uvicorn httpx discord.py
```

Attendi la fine dell’installazione.

---

# 📌 Passo 6 – Avvia il progetto

Apri **due** finestre del terminale.

### 🖥️ Terminale 1 – Avvia il bot

```bash
python bot.py
```

Dovresti vedere:

```
Bot online come ItalyRP Bot
```

### 🌐 Terminale 2 – Avvia il sito web

```bash
python server.py
```

Dovresti vedere:

```
Italy RP Portal avviato su http://127.0.0.1:8000
```

---

# 📌 Passo 7 – Apri il portale

Apri il browser e vai su:

```
http://localhost:8000
```

Clicca **Accedi con Discord** → Autorizza.

---

# 🤖 Comandi principali del bot

| Comando | Descrizione |
|----------|-------------|
| `/info` | Info del server |
| `/profilo` | Profilo utente |
| `/regole` | Regolamento |
| `/ping` | Latenza |
| `/premium @utente` | Dai premium |
| `/leva_premium @utente` | Togli premium |
| `/warn @utente motivo` | Warn |
| `/kick @utente motivo` | Kick |
| `/ban @utente motivo` | Ban |
| `/muto @utente minuti motivo` | Timeout |
| `/purge numero` | Cancella messaggi |
| `/ruolo_dai @utente @ruolo` | Assegna ruolo |
| `/ruolo_togli @utente @ruolo` | Rimuove ruolo |

---

# 🆘 Supporto

👉 **Discord:** [https://discord.gg/ZQBGEnfMfC](https://discord.gg/ZQBGEnfMfC)

---

<div align="center">

🔥 **Buon divertimento con Italy RP Portal!** 🔥

</div>
