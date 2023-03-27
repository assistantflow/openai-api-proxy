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
        return JSONResponse(content={"error": {"message": f"request {httpxClient._base_url} failed"}}, status_code=500)


# The OpenAI API as of March 27th, 2023.
@app.api_route("/v1/models", methods=["GET", "OPTIONS"])
@app.api_route("/v1/models/{model}", methods=["GET", "DELETE", "OPTIONS"])
@app.api_route("/v1/completions", methods=["POST", "OPTIONS"])
@app.api_route("/v1/chat/completions", methods=["POST", "OPTIONS"])
@app.api_route("/v1/edits", methods=["POST", "OPTIONS"])
@app.api_route("/v1/images/generations", methods=["POST", "OPTIONS"])
@app.api_route("/v1/images/edits", methods=["POST", "OPTIONS"])
@app.api_route("/v1/images/variations", methods=["POST", "OPTIONS"])
@app.api_route("/v1/embeddings", methods=["POST", "OPTIONS"])
@app.api_route("/v1/audio/transcriptions", methods=["POST", "OPTIONS"])
@app.api_route("/v1/audio/translations", methods=["POST", "OPTIONS"])
@app.api_route("/v1/files", methods=["GET", "POST", "OPTIONS"])
@app.api_route("/v1/files/{file_id}", methods=["GET", "DELETE", "OPTIONS"])
@app.api_route("/v1/files/{file_id}/content", methods=["GET", "OPTIONS"])
@app.api_route("/v1/fine-tunes", methods=["GET", "POST", "OPTIONS"])
@app.api_route("/v1/fine-tunes/{fine_tune_id}", methods=["GET", "OPTIONS"])
@app.api_route("/v1/fine-tunes/{fine_tune_id}/cancel", methods=["POST", "OPTIONS"])
@app.api_route("/v1/fine-tunes/{fine_tune_id}/events", methods=["GET", "OPTIONS"])
@app.api_route("/v1/moderations", methods=["POST", "OPTIONS"])
@app.api_route("/v1/engines", methods=["GET", "OPTIONS"])
@app.api_route("/v1/engines/{engine_id}", methods=["GET", "OPTIONS"])
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
