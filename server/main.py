import httpx
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.background import BackgroundTasks


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    global httpxClient
    httpxClient = httpx.AsyncClient(base_url="https://api.openai.com", timeout=60)


@app.on_event("shutdown")
async def shutdown_event():
    await httpxClient.aclose()


@app.api_route("/v1/completions", methods=["GET", "POST", "OPTIONS"])
@app.api_route("/v1/chat/completions", methods=["GET", "POST", "OPTIONS"])
async def proxy(req: Request):
    nh = req.headers.mutablecopy()
    nh["host"] = httpxClient._base_url.host
    req._headers = nh
    req.scope.update(headers=req.headers.raw)

    url = httpx.URL(path=req.url.path, query=req.url.query.encode("utf-8"))
    br = httpxClient.build_request(req.method, url, headers=req.headers.raw, content=await req.body())
    resp = await httpxClient.send(br, stream=True)

    return StreamingResponse(
        resp.aiter_raw(),
        status_code=resp.status_code,
        headers=resp.headers,
        background=BackgroundTasks([resp.aclose])
    )


def start():
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)
