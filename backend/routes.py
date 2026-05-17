from fastapi import APIRouter
import upload
import query
import analysis
import auth


router = APIRouter()

router.include_router(auth.router)
router.include_router(upload.router)
router.include_router(query.router)
router.include_router(analysis.router)

@router.get("/health")
def health_check():
    return {"status": "ok"}