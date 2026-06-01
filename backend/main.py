from fastapi import FastAPI
from routers import alerts,analyze

app = FastAPI(title="CodeGuard API", version="1.0")

# חיבור הראוטרים לשרת
app.include_router(alerts.router)
app.include_router(analyze.router)


@app.get("/")
def read_root():
    return {"message": "CodeGuard Server is Up and Running!"}