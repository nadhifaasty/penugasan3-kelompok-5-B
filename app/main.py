from fastapi import FastAPI
from app.routers import role_router, user_router, account_router, registration_router, event_router
from app.database import engine, Base 
from fastapi.middleware.cors import CORSMiddleware

import app.models 

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRUD API", version="1.0.0")

# Register Router
app.include_router(role_router.router)
app.include_router(user_router.router)
app.include_router(account_router.router)
app.include_router(registration_router.router)
app.include_router(event_router.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)