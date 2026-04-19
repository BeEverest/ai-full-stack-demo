from sqlalchemy.ext.asyncio import AsyncSession
from app.models.domain.contact import ContactSubmission
from app.models.schemas.contact import ContactIn


async def create_contact_submission(
    db: AsyncSession,
    payload: ContactIn,
    ip_address: str | None,
) -> ContactSubmission:
    submission = ContactSubmission(
        name=payload.name,
        email=payload.email,
        company=payload.company,
        inquiry_type=payload.inquiry_type,
        message=payload.message,
        ip_address=ip_address,
    )
    db.add(submission)
    await db.commit()
    return submission
