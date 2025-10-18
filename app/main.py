from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote
from . import migrate_and_seed
from .config import settings

migrate_and_seed.run()

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc"
)

origins = ["*"] # Allow all origins for simplicity; adjust in production

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!",
            "docs_url": f"{settings.API_PREFIX}/docs",
            "redoc_url": f"{settings.API_PREFIX}/redoc"}    

@app.get("/health")
async def health_check():
    return {"status": "healthy"}