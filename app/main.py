from fastapi import FastAPI
from .seed import seed_data
from .routers import post, user, auth

seed_data()

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)



