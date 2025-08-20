from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

from .api.routes import auth, category, warning, graphql

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(category.router)
app.include_router(warning.router)
app.include_router(graphql.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}