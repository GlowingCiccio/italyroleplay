import httpx
import os
import json
import datetime
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Italy RP Portal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CLIENT_ID     = "INSERISCI"
CLIENT_SECRET = "INSERISCI"
REDIRECT_URI  = "INSERISCI"
BOT_TOKEN     = "INSERISCI"
GUILD_ID      = "INSERISCI"
ROLE_MEMBRO   = "INSERISCI"
DISCORD_API   = "INSERISCI"

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/login")
def login():
    url = (
        f"{DISCORD_API}/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify%20guilds.join%20guilds"
    )
    return RedirectResponse(url)

async def add_user_to_guild(access_token: str, user_id: str):
    url = f"{DISCORD_API}/guilds/{GUILD_ID}/members/{user_id}"
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "access_token": access_token,
        "roles": [ROLE_MEMBRO]
    }
    async with httpx.AsyncClient() as client:
        r = await client.put(url, headers=headers, json=data)
        return r.status_code

@app.get("/callback")
async def callback(code: str):
    async with httpx.AsyncClient() as client:
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

        user_res = await client.get(
            f"{DISCORD_API}/users/@me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user = user_res.json()

        status = await add_user_to_guild(access_token, user["id"])

    params = (
        f"?user={user['username']}"
        f"&avatar={user.get('avatar', '')}"
        f"&id={user['id']}"
        f"&status={status}"
    )
    return RedirectResponse(f"/{params}")

@app.get("/api/guild")
async def api_guild():
    """Restituisce info base del guild (usato dal frontend per le statistiche)"""
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

@app.get("/api/roles")
async def api_roles():
    """Lista ruoli del guild"""
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bot {BOT_TOKEN}"}
        r = await client.get(f"{DISCORD_API}/guilds/{GUILD_ID}/roles", headers=headers)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="Errore API Discord")
        roles = r.json()
        public_roles = [
            {"id": ro["id"], "name": ro["name"], "color": ro["color"]}
            for ro in roles
            if ro["name"] != "@everyone" and not ro["managed"]
        ]
        return public_roles

@app.get("/api/health")
async def health():
    return {"status": "ok", "timestamp": datetime.datetime.utcnow().isoformat()}

if __name__ == "__main__":
    print("🚀 Italy RP Portal avviato!")
    print("🌐 Apri il browser su: http://127.0.0.1:8000")
    print("🔗 Login Discord:      http://127.0.0.1:8000/login")
    print("─" * 45)
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)