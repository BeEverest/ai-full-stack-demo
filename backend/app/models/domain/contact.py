from datetime import datetime
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class ContactSubmission(Base):
    __tablename__ = "contact_submissions"

    id           : Mapped[int]        = mapped_column(primary_key=True, autoincrement=True)
    name         : Mapped[str]        = mapped_column(String(100))
    email        : Mapped[str]        = mapped_column(String(254))
    company      : Mapped[str]        = mapped_column(String(200), default="")
    inquiry_type : Mapped[str]        = mapped_column(String(20), default="other")
    message      : Mapped[str]        = mapped_column(Text)
    status       : Mapped[str]        = mapped_column(String(20), default="pending")
    ip_address   : Mapped[str | None] = mapped_column(String(45), nullable=True)
    submitted_at : Mapped[datetime]   = mapped_column(DateTime, default=datetime.utcnow)
    updated_at   : Mapped[datetime]   = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    notes        : Mapped[str]        = mapped_column(Text, default="")
