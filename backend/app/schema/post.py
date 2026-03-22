from pydantic import BaseModel, ConfigDict


class PostCreate(BaseModel):
    title: str
    slug: str
    content: str | None = None

class PostUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    content: str | None = None

class PostView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    content: str | None = None
