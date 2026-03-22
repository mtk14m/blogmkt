from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.post import Post
from app.schema.post import PostView
from app.schema.post import PostCreate
from app.schema.post import PostUpdate

router=APIRouter(prefix="/posts")

@router.get("/")
def list_posts(postView: PostView, db: Session = Depends(get_db)):
    posts = db.query(Post).all
    return [mapper_post_to_postView(post) for post in posts]

@router.get("/{slug}")
def get_post_by_id(slug: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(slug=slug).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return mapper_post_to_postView(post)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(playload: PostCreate, db: Session = Depends(get_db)):
    existing_post = db.query(Post).filter(Post.slug==playload.slug).first()
    if existing_post:
        raise HTTPException(status_code=400, detail="Slug already exist")
    
    post = Post(
        title=playload.title,
        slug=playload.slug,
        content=playload.content
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return post

@router.put("/{slug}")
def update_post(slug: str, payload: PostUpdate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.slug==slug).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if payload.slug and payload.slug == slug:
        existing_post = db.query(Post).filter(Post.slug==slug).first()
        if existing_post:
            raise HTTPException(status_code=400, detail="Slug already exists")
        
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(post, field, value)
    
    db.commit()
    db.refresh(post)

    return post 



#NOTE: mapper, faudrait peut être les mettre ailleur
def mapper_post_to_postView(post: Post)->PostView:
    return PostView(
        title=post.title,
        slug=post.slug,
        content=post.content
    )