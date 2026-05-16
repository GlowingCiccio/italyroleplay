<div align="center">
  
  <img src="https://cdn.discordapp.com/icons/1431571702747238463/your_server_icon.png" width="150" style="border-radius: 50%;">
  
  # 🇮🇹 Italy RP Portal
  
  ### Sistema completo di gestione Discord + Portale Web Premium
  
  [![Discord](https://img.shields.io/badge/Discord-Join-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/ZQBGEnfMfC)
  [![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
  [![Discord.py](https://img.shields.io/badge/Discord.py-2.3+-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io)
  
  <p align="center">
    <strong>✨ Portale avanzato per la gestione del tuo server Discord FiveM ✨</strong>
  </p>
  
  ![Preview](https://via.placeholder.com/800x400/1a1a2e/5c6ef5?text=Italy+RP+Portal+Preview)
  
</div>

---

## 📋 Tabella dei Contenuti

- [🎯 Caratteristiche](#-caratteristiche)
- [✨ Funzioni Premium](#-funzioni-premium)
- [🤖 Comandi Bot](#-comandi-bot)
- [🛠️ Tecnologie Utilizzate](#️-tecnologie-utilizzate)
- [📦 Installazione](#-installazione)
- [⚙️ Configurazione](#️-configurazione)
- [🚀 Avvio](#-avvio)
- [📁 Struttura del Progetto](#-struttura-del-progetto)
- [🔧 API Endpoints](#-api-endpoints)
- [🎮 Comandi Discord](#-comandi-discord)
- [🔐 Permessi Richiesti](#-permessi-richiesti)
- [🐛 Risoluzione Problemi](#-risoluzione-problemi)
- [📝 Licenza](#-licenza)
- [💬 Supporto](#-supporto)

---

## 🎯 Caratteristiche

### 🤖 Bot Discord
- ✅ **Sistema di Warn** (3 warn = kick automatico)
- ✅ **Moderazione completa** (kick, ban, mute, purge)
- ✅ **Gestione ruoli** (assegna/rimuovi ruoli)
- ✅ **Sistema Ticket integrato**
- ✅ **Logging dettagliato** di tutte le azioni
- ✅ **Benvenuto automatico** con ruolo membro
- ✅ **Comandi informativi** (ping, info, profilo, regole)
- ✅ **Sistema Premium** con ruoli dedicati

### 🌐 Portale Web
- ✅ **Login con Discord OAuth2**
- ✅ **Profilo utente in tempo reale**
- ✅ **Statistiche server live** (membri totali, online)
- ✅ **Design moderno con glassmorphism**
- ✅ **Responsive** (funziona su mobile/tablet/desktop)
- ✅ **Funzioni premium dinamiche** (appaiono/scompaiono in tempo reale)
- ✅ **API REST completa**
- ✅ **Check premium automatico ogni 15 secondi**

---

## ✨ Funzioni Premium

Quando un utente riceve il ruolo premium su Discord, il portale sblocca automaticamente:

| Funzione | Descrizione |
|----------|-------------|
| 📊 **Dashboard Avanzata** | Analisi dettagliata delle attività di gioco |
| 👤 **Analisi Giocatore** | Statistiche personalizzate sul gameplay |
| 🛡️ **Strumenti Staff Premium** | Accesso a tool esclusivi |
| ⏰ **Accesso Anticipato** | Partecipa agli eventi prima di tutti |
| 💾 **Backup Dedicati** | Salvataggio automatico dei progressi |
| 🎨 **Colori Personalizzati** | Temi esclusivi per il portale |
| 🏆 **Badge Premium** | Icona esclusiva sul profilo |

> **Nota:** Le funzioni premium vengono mostrate/nascondono automaticamente quando il ruolo viene assegnato o rimosso su Discord!

---

## 🤖 Comandi Bot

### 👤 Comandi Generali
| Comando | Descrizione |
|---------|-------------|
| `/ping` | Mostra la latenza del bot |
| `/info` | Mostra le informazioni del server |
| `/profilo` | Visualizza il tuo profilo nel server |
| `/regole` | Mostra il regolamento del server |
| `/miei_warns` | Visualizza i tuoi warn |
| `/ticket` | Info su come aprire un ticket |

### ⚠️ Comandi Staff
| Comando | Descrizione |
|---------|-------------|
| `/warn <membro> <motivo>` | Assegna un warn a un membro |
| `/warn_lista <membro>` | Visualizza i warn di un membro |
| `/warn_rimuovi <membro>` | Rimuove l'ultimo warn |
| `/kick <membro> <motivo>` | Espelle un membro |
| `/ban <membro> <motivo>` | Banna un membro |
| `/muto <membro> <minuti> <motivo>` | Mette in timeout un membro |
| `/smuto <membro>` | Rimuove il timeout |
| `/purge <quantità>` | Elimina messaggi in massa |
| `/ruolo_dai <membro> <ruolo>` | Assegna un ruolo |
| `/ruolo_togli <membro> <ruolo>` | Rimuove un ruolo |
| `/slowmode <secondi>` | Imposta slowmode nel canale |

### 👑 Comandi Admin
| Comando | Descrizione |
|---------|-------------|
| `/unban <user_id> <motivo>` | Rimuove il ban di un utente |
| `/annuncio <canale> <titolo> <testo>` | Invia un annuncio embed |
| `/premium <membro>` | Assegna il premium a un utente |
| `/leva_premium <membro>` | Rimuove il premium da un utente |

---

## 🛠️ Tecnologie Utilizzate

<div align="center">
  
  ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
  ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
  ![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)
  ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
  ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
  ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
  
</div>

- **Backend:** FastAPI, Uvicorn, HTTPX
- **Bot:** Discord.py 2.3+
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Autenticazione:** Discord OAuth2
- **API:** RESTful

---

## 📦 Installazione

### Prerequisiti

- Python 3.9 o superiore
- Un server Discord con permessi di amministratore
- Un'applicazione Discord (per OAuth2)
- Token del bot Discord

### Passaggi

1. **Clona il repository**
```bash
git clone https://github.com/tuo-username/italy-rp-portal.git
cd italy-rp-portal
