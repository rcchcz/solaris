import uvicorn
from fastapi import FastAPI
from client.routers import client_router
# from shared.database import engine, Base
# from client.models.client_model import Client

# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(client_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3030)