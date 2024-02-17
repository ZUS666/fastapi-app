from fastapi import APIRouter

router = APIRouter(prefix='/users')


@router.get('/')
async def get_users():
    """Get collection of users"""
    pass
