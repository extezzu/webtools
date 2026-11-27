"""Minimal FastAPI example: refresh token rotation with reuse detection.

In-memory store for clarity. In production keep the token records in a database
(see README). MIT licensed.
"""
import time
import uuid

import jwt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

SECRET = "change-me-in-production"
ALGO = "HS256"
ACCESS_TTL = 15 * 60
REFRESH_TTL = 7 * 24 * 3600

app = FastAPI()
# jti -> {"family": str, "user": str, "revoked": bool}
TOKENS: dict[str, dict] = {}


class Login(BaseModel):
    username: str


class Refresh(BaseModel):
    refresh_token: str


def _pair(user: str, family: str | None = None) -> dict:
    now = int(time.time())
    family = family or uuid.uuid4().hex
    jti = uuid.uuid4().hex
    TOKENS[jti] = {"family": family, "user": user, "revoked": False}
    refresh = jwt.encode(
        {"sub": user, "type": "refresh", "jti": jti, "fam": family, "iat": now, "exp": now + REFRESH_TTL},
        SECRET, algorithm=ALGO)
    access = jwt.encode(
        {"sub": user, "type": "access", "iat": now, "exp": now + ACCESS_TTL}, SECRET, algorithm=ALGO)
    return {"access_token": access, "refresh_token": refresh}


@app.post("/login")
def login(data: Login):
    # Demo only: real code verifies a password hash here.
    return _pair(data.username)


@app.post("/refresh")
def refresh(data: Refresh):
    bad = HTTPException(401, "Invalid refresh token")
    try:
        payload = jwt.decode(data.refresh_token, SECRET, algorithms=[ALGO])
    except jwt.PyJWTError:
        raise bad from None
    if payload.get("type") != "refresh":
        raise bad
    row = TOKENS.get(payload["jti"])
    if row is None:
        raise bad
    if row["revoked"]:
        # Reuse detected: assume theft, revoke the whole family.
        for r in TOKENS.values():
            if r["family"] == row["family"]:
                r["revoked"] = True
        raise bad
    row["revoked"] = True
    return _pair(row["user"], family=row["family"])
