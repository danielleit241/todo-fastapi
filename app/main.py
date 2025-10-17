from fastapi import FastAPI, HTTPException
from typing import Optional

from pydantic import BaseModel

app = FastAPI()

class Blog(BaseModel): 
    id: int
    title: str
    body: str
    published: bool = True
    vote: Optional[int] = None

blogs = [
    Blog(id=1, title="First Blog", body="This is the body of the first blog", published=True, vote=10),
    Blog(id=2, title="Second Blog", body="This is the body of the second blog", published=False),
    Blog(id=3, title="Third Blog", body="This is the body of the third blog", published=True, vote=5),
]

def find_blog(id: int):
    for blog in blogs:
        if blog.id == id:
            return blog
    return None

@app.get("/blogs", response_model=list[Blog])
def read_blogs():
    return blogs

@app.get("/blogs/{id}")
def read_blog(id: int):
    blog = find_blog(id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.post("/blogs")
def create_blog(blog: Blog):
    blogs.append(blog)
    return blog

@app.put("/blogs/{id}")
def update_blog(id: int, updated_blog: Blog):
    blog = find_blog(id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog.title = updated_blog.title
    blog.body = updated_blog.body
    blog.published = updated_blog.published
    blog.vote = updated_blog.vote
    return blog

@app.delete("/blogs/{id}")
def delete_blog(id: int):
    blog = find_blog(id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blogs.remove(blog)
    return {"detail": "Blog deleted"}