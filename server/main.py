from urllib.parse import urlparse
from starlette.background import BackgroundTask
import aiohttp
import uvicorn
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse


app = FastAPI()
aiohttpClient: aiohttp.ClientSession = None


@app.on_event("startup")
async def startup_event():
    global aiohttpClient
    aiohttpClient = aiohttp.ClientSession(base_url="https://api.openai.com", timeout=aiohttp.ClientTimeout(total=30))


@app.on_event("shutdown")
async def shutdown_event():
    await aiohttpClient.close()


@app.api_route("/v1/completions", methods=["GET", "POST", "OPTIONS"])
@app.api_route("/v1/chat/completions", methods=["GET", "POST", "OPTIONS"])
async def proxy(req: Request) -> EventSourceResponse:
    _headers = req.headers.mutablecopy()
    _headers["host"] = aiohttpClient._base_url.host
    req._headers = _headers
    req.scope.update(headers=req.headers.raw)

    if req.method == "OPTIONS":
        body = None
    else:
        body = await req.json()
    resp = await aiohttpClient.request(req.method, req.url.path, headers=req.headers, json=body)

    async def event_generator():
        while line := await resp.content.readline():
            yield line

    return EventSourceResponse(
        event_generator(), status_code=resp.status, headers=resp.headers, background=BackgroundTask(resp.close)
    )


def start():
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)
