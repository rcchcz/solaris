import uvicorn
from fastapi import FastAPI
from client.routers import client_router

app = FastAPI()

app.include_router(client_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3030)