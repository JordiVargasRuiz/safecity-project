from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI(title="Users & Auth Service")

users_db = {
    "admin": {"username": "admin", "password": "admin123"}
}

@app.get("/")
def read_root():
    return {"service": "Users & Auth", "status": "active"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return {"access_token": "token-seguro-safecity-2026", "token_type": "bearer"}