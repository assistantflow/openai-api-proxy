import click
import httpx
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.background import BackgroundTasks


app = FastAPI()
httpxClient: httpx.AsyncClient = None


@app.on_event("startup")
async def startup_event():
    global httpxClient
    httpxClient = httpx.AsyncClient(base_url="https://api.openai.com", timeout=60)


@app.on_event("shutdown")
async def shutdown_event():
    await httpxClient.aclose()


@app.middleware("http")
async def catch_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        return JSONResponse(content={"message": f"request {httpxClient._base_url} failed"}, status_code=500)


@app.api_route("/v1/completions", methods=["GET", "POST", "OPTIONS"])
@app.api_route("/v1/chat/completions", methods=["GET", "POST", "OPTIONS"])
async def proxy(req: Request) -> StreamingResponse:
    nh = req.headers.mutablecopy()
    nh["host"] = httpxClient._base_url.host
    req._headers = nh
    req.scope.update(headers=req.headers.raw)

    url = httpx.URL(path=req.url.path, query=req.url.query.encode("utf-8"))
    br = httpxClient.build_request(req.method, url, headers=req.headers.raw, content=await req.body())
    resp = await httpxClient.send(br, stream=True)

    async def echo():
        async for line in resp.aiter_lines():
            yield line

    return StreamingResponse(
        echo(), status_code=resp.status_code, headers=resp.headers, background=BackgroundTasks([resp.aclose])
    )


@click.command
@click.option("--port", default=8000, help="the server port", show_default=True)
@click.option("--reload", default=False, help="enable reload mode for development", show_default=True)
def start(port: int, reload: bool):
    uvicorn.run("server.main:app", host="0.0.0.0", port=port, reload=reload)
