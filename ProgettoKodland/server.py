import httpx
import os
import json
import datetime
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI(title="Italy RP Portal - Premium Edition")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# CONFIGURAZIONE - VERIFICA I TUOI ID!
# ============================================
CLIENT_ID = "INSERISCI"
CLIENT_SECRET = "INSERISCI"
REDIRECT_URI = "INSERISCI"
BOT_TOKEN = "INSERISCI"
GUILD_ID = "INSERISCI"
ROLE_MEMBRO = "INSERISCI"
ROLE_PREMIUM_ID = "INSERISCI"  
DISCORD_API = "https://discord.com/api/v10"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

# ============================================
# FUNZIONE PER VERIFICARE PREMIUM (MIGLIORATA)
# ============================================
async def check_user_premium(user_id: str) -> bool:
    """Verifica se un utente ha il ruolo premium su Discord"""
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bot {BOT_TOKEN}"}
        url = f"{DISCORD_API}/guilds/{GUILD_ID}/members/{user_id}"
        
        print(f"🔍 Verifico premium per user {user_id}...")
        
        try:
            r = await client.get(url, headers=headers)
            print(f"📡 Status code: {r.status_code}")
            
            if r.status_code == 200:
                data = r.json()
                roles = data.get("roles", [])
                print(f"🎭 Ruoli dell'utente: {roles}")
                print(f"🏷️ Ruolo premium cercato: {ROLE_PREMIUM_ID}")
                
                # Converti in stringa per confronto sicuro
                has_premium = str(ROLE_PREMIUM_ID) in [str(role) for role in roles]
                print(f"💎 Ha premium: {has_premium}")
                return has_premium
            else:
                print(f"❌ Errore: {r.text}")
                return False
        except Exception as e:
            print(f"🔥 Errore nel check premium: {e}")
            return False

async def add_user_to_guild(access_token: str, user_id: str):
    url = f"{DISCORD_API}/guilds/{GUILD_ID}/members/{user_id}"
    headers = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}
    data = {"access_token": access_token, "roles": [ROLE_MEMBRO]}
    async with httpx.AsyncClient() as client:
        r = await client.put(url, headers=headers, json=data)
        print(f"➕ Aggiunta utente al server: status {r.status_code}")
        return r.status_code

# ============================================
# ROTTE
# ============================================
@app.get("/", response_class=HTMLResponse)
async def root():
    if not os.path.exists(INDEX_PATH):
        return HTMLResponse("<h1>ERRORE: index.html non trovato</h1>", status_code=500)
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/login")
def login():
    url = (f"{DISCORD_API}/oauth2/authorize"
           f"?client_id={CLIENT_ID}"
           f"&redirect_uri={REDIRECT_URI}"
           f"&response_type=code"
           f"&scope=identify%20guilds.join%20guilds")
    return RedirectResponse(url)

@app.get("/callback")
async def callback(code: str):
    async with httpx.AsyncClient() as client:
        # Scambio token
        token_res = await client.post(
            f"{DISCORD_API}/oauth2/token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if token_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Token exchange fallito")

        token_data = token_res.json()
        access_token = token_data.get("access_token")

        # Ottieni utente
        user_res = await client.get(
            f"{DISCORD_API}/users/@me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if user_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Impossibile ottenere i dati utente")

        user = user_res.json()
        user_id = user["id"]

        # Aggiungi al server
        status = await add_user_to_guild(access_token, user_id)

        # VERIFICA PREMIUM (FONDAMENTALE!)
        is_premium = await check_user_premium(user_id)
        
        print(f"✨ Utente {user['username']} - Premium: {is_premium}")

        # Reindirizza con i parametri
        params = (f"?user={user['username']}"
                  f"&avatar={user.get('avatar', '')}"
                  f"&id={user_id}"
                  f"&status={status}"
                  f"&premium={'1' if is_premium else '0'}")
        
        redirect_url = f"/{params}"
        print(f"🔄 Redirect a: {redirect_url}")
        return RedirectResponse(redirect_url)

@app.get("/api/me/premium")
async def api_me_premium(user_id: str = Query(..., description="ID utente Discord")):
    """Endpoint per verificare lo stato premium in tempo reale"""
    is_premium = await check_user_premium(user_id)
    print(f"📊 API premium check: user {user_id} -> {is_premium}")
    return {"premium": is_premium, "user_id": user_id}

@app.get("/api/guild")
async def api_guild():
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bot {BOT_TOKEN}"}
        r = await client.get(f"{DISCORD_API}/guilds/{GUILD_ID}?with_counts=true", headers=headers)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="Errore API Discord")
        data = r.json()
        return {
            "name": data.get("name"),
            "icon": data.get("icon"),
            "member_count": data.get("approximate_member_count", 0),
            "online_count": data.get("approximate_presence_count", 0),
            "guild_id": GUILD_ID,
        }

@app.get("/api/health")
async def health():
    return {"status": "ok", "timestamp": datetime.datetime.utcnow().isoformat()}

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Italy RP Portal Premium avviato!")
    print(f"📁 Directory: {BASE_DIR}")
    print(f"🌐 http://127.0.0.1:8000")
    print(f"🔗 Login: http://127.0.0.1:8000/login")
    print("=" * 50)
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)