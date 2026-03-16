from fastapi import APIRouter

router=APIRouter(prefix="/posts")

@router.get("/")
def home():
    return {"home": "tous les posts"}