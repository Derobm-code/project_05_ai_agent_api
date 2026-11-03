
import hashlib
import os
import time

import httpx
from fastapi import HTTPException, Request

LIMIT = 10
WINDOW_SECONDS = 3600

LUA_SCRIPT = """
local count = redis.call('INCR', KEYS[1])
if count == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end
return count
"""


def enforce_rate_limit(request: Request) -> None:
    url = os.getenv("UPSTASH_REDIS_REST_URL")
    token = os.getenv("UPSTASH_REDIS_REST_TOKEN")

    # Fail closed if protection is not configured.
    if not url or not token:
        raise HTTPException(
            status_code=503,
            detail="Rate limiting is not configured.",
        )

    # Vercel normally forwards the visitor's IP address.
    forwarded = request.headers.get("x-forwarded-for", "")
    ip = forwarded.split(",")[0].strip()

    if not ip:
        ip = request.client.host if request.client else "unknown"

    ip_hash = hashlib.sha256(ip.encode()).hexdigest()
    window = int(time.time()) // WINDOW_SECONDS
    key = f"ai-agent:rate:{ip_hash}:{window}"

    try:
        response = httpx.post(
            url.rstrip("/"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json=[
                "EVAL",
                LUA_SCRIPT,
                "1",
                key,
                str(WINDOW_SECONDS + 60),
            ],
            timeout=5,
        )
        response.raise_for_status()
        payload = response.json()

        if payload.get("error"):
            raise ValueError(payload["error"])

        count = int(payload["result"])

    except (httpx.HTTPError, ValueError, KeyError, TypeError):
        raise HTTPException(
            status_code=503,
            detail="Request protection is temporarily unavailable.",
        )

    if count > LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Rate limit reached. Please try again later.",
            headers={"Retry-After": str(WINDOW_SECONDS)},
        )
