from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.crud.contact_crud import create_contact_submission
from app.models.schemas.contact import ContactIn, ContactOut

router = APIRouter()


@router.post("", response_model=ContactOut)
async def submit_contact(
    payload: ContactIn,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    ip_address = request.client.host if request.client else None
    await create_contact_submission(db, payload, ip_address)
    return ContactOut(success=True, message="提交成功，我们将在24小时内与您联系")
