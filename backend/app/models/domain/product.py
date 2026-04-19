from datetime import datetime
from sqlalchemy import String, Text, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id          : Mapped[int]      = mapped_column(primary_key=True, autoincrement=True)
    slug        : Mapped[str]      = mapped_column(String(50), unique=True, index=True)
    category    : Mapped[str]      = mapped_column(String(20))
    name        : Mapped[str]      = mapped_column(String(100))
    tagline     : Mapped[str]      = mapped_column(String(200))
    description : Mapped[str]      = mapped_column(Text)
    cover_image : Mapped[str]      = mapped_column(String(500))
    is_active   : Mapped[bool]     = mapped_column(Boolean, default=True)
    sort_order  : Mapped[int]      = mapped_column(Integer, default=0)
    created_at  : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at  : Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    features : Mapped[list["ProductFeature"]] = relationship(
        back_populates="product",
        order_by="ProductFeature.sort_order",
        cascade="all, delete-orphan",
    )
    specs    : Mapped[list["ProductSpec"]]    = relationship(
        back_populates="product",
        order_by="ProductSpec.sort_order",
        cascade="all, delete-orphan",
    )
    images   : Mapped[list["ProductImage"]]   = relationship(
        back_populates="product",
        order_by="ProductImage.sort_order",
        cascade="all, delete-orphan",
    )


class ProductFeature(Base):
    __tablename__ = "product_features"

    id          : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id  : Mapped[int] = mapped_column(ForeignKey("products.id"))
    icon        : Mapped[str] = mapped_column(String(100))
    title       : Mapped[str] = mapped_column(String(100))
    description : Mapped[str] = mapped_column(String(300))
    sort_order  : Mapped[int] = mapped_column(Integer, default=0)

    product : Mapped["Product"] = relationship(back_populates="features")


class ProductSpec(Base):
    __tablename__ = "product_specs"

    id         : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.id"))
    spec_key   : Mapped[str] = mapped_column(String(100))
    spec_value : Mapped[str] = mapped_column(String(200))
    sort_order : Mapped[int] = mapped_column(Integer, default=0)

    product : Mapped["Product"] = relationship(back_populates="specs")


class ProductImage(Base):
    __tablename__ = "product_images"

    id         : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.id"))
    image_url  : Mapped[str] = mapped_column(String(500))
    alt_text   : Mapped[str] = mapped_column(String(200), default="")
    sort_order : Mapped[int] = mapped_column(Integer, default=0)

    product : Mapped["Product"] = relationship(back_populates="images")


class SiteStat(Base):
    __tablename__ = "site_stats"

    id         : Mapped[int]  = mapped_column(primary_key=True, autoincrement=True)
    label      : Mapped[str]  = mapped_column(String(100))
    value      : Mapped[str]  = mapped_column(String(50))
    unit       : Mapped[str]  = mapped_column(String(50), default="")
    sort_order : Mapped[int]  = mapped_column(Integer, default=0)
    is_active  : Mapped[bool] = mapped_column(Boolean, default=True)
