from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def public_root():
    return {"message": "Este es un endpoint público", "status": "ok"}
