from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLIENT_ID     = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI  = os.getenv("REDIRECT_URI")
BOT_SECRET    = os.getenv("BOT_SECRET")
DISCORD_API   = os.getenv("DISCORD_API")

premium_users: set[str] = set()
sessions: dict[str, str] = {}


@app.get("/login")
def login():
    url = (
        f"{DISCORD_API}/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify"
    )
    return RedirectResponse(url)


@app.get("/callback")
async def callback(code: str):
    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            f"{DISCORD_API}/oauth2/token",
            data={
                "client_id":     CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type":    "authorization_code",
                "code":          code,
                "redirect_uri":  REDIRECT_URI,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token_data = token_res.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="Token non valido")

        user_res = await client.get(
            f"{DISCORD_API}/users/@me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user = user_res.json()
        user_id = user["id"]

    sessions[access_token] = user_id
    return RedirectResponse(f"http://127.0.0.1:8000/?token={access_token}")


@app.get("/me")
async def me(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user_id = sessions.get(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Non autenticato")

    async with httpx.AsyncClient() as client:
        user_res = await client.get(
            f"{DISCORD_API}/users/@me",
            headers={"Authorization": f"Bearer {token}"},
        )
        user = user_res.json()

    return {
        "id":       user["id"],
        "username": user["username"],
        "avatar":   user.get("avatar"),
        "premium":  user_id in premium_users,
    }


@app.post("/set-premium")
async def set_premium(request: Request):
    if request.headers.get("X-Bot-Secret", "") != BOT_SECRET:
        raise HTTPException(status_code=403, detail="Non autorizzato")

    body = await request.json()
    user_id = str(body.get("user_id", ""))
    action  = body.get("action", "add")

    if not user_id:
        raise HTTPException(status_code=400, detail="user_id mancante")

    if action == "add":
        premium_users.add(user_id)
    elif action == "remove":
        premium_users.discard(user_id)
    else:
        raise HTTPException(status_code=400, detail="action non valida")

    return {"status": "ok"}




@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)