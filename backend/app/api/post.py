from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.post import Post
from app.schema.post import PostCreate, PostUpdate, PostView

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[PostView])
def list_posts(db: Session = Depends(get_db)) -> list[Post]:
    return db.query(Post).order_by(Post.id.desc()).all()


@router.get("/{slug}", response_model=PostView)
def get_post_by_id(slug: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.slug == slug).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/", response_model=PostView, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, db: Session = Depends(get_db)) -> Post:
    existing_post = db.query(Post).filter(Post.slug == payload.slug).first()
    if existing_post:
        raise HTTPException(status_code=400, detail="Slug already exists")

    post = Post(
        title=payload.title,
        slug=payload.slug,
        content=payload.content,
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@router.put("/{slug}", response_model=PostView)
def update_post(slug: str, payload: PostUpdate, db: Session = Depends(get_db)) -> Post:
    post = db.query(Post).filter(Post.slug == slug).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if payload.slug and payload.slug != slug:
        existing_post = db.query(Post).filter(Post.slug == payload.slug).first()
        if existing_post:
            raise HTTPException(status_code=400, detail="Slug already exists")

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)

    return post


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(slug: str, db: Session = Depends(get_db)) -> None:
    post = db.query(Post).filter(Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
