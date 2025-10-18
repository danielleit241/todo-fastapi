from asyncio import subprocess
from fastapi import FastAPI
from .routers import post, user, auth, vote

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

def startup_event():
    subprocess.run(["python", "app/migrate_and_seed.py"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)



