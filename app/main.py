from fastapi import FastAPI

app = FastAPI(
    title="Stumi",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to Stumi"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
