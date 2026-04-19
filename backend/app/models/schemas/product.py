from pydantic import BaseModel, ConfigDict
from typing import List


class FeatureOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    icon: str
    title: str
    description: str


class SpecOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    spec_key: str
    spec_value: str


class ImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    image_url: str
    alt_text: str


class ProductListOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    slug: str
    category: str
    name: str
    tagline: str
    cover_image: str


class ProductDetailOut(ProductListOut):
    description: str
    features: List[FeatureOut]
    specs: List[SpecOut]
    images: List[ImageOut]


class StatOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    label: str
    value: str
    unit: str
