from fastapi import FastAPI
import uvicorn

from app.api.auth import router as auth_router
from app.api.post import router as posts_router

app = FastAPI(title="BLOGMKT API", description="L'api de mon blog personnel")

app.include_router(auth_router)
app.include_router(posts_router)

def main():
    uvicorn.run("main:app", reload=True)

@app.get("/health", tags=["health"])
def heath_check():
    return {"status": "ok"}


if __name__ == "__main__":
    main()
