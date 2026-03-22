from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    slug: str
    content: str | None = None

class PostUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    content: str | None = None

class PostView(BaseModel):
    title: str
    slug: str
    content: str | None = None

