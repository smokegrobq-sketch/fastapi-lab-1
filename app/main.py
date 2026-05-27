from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Lab 1",
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "FastAPI template is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


def start() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
