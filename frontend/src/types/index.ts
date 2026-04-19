export interface Product {
  slug: string
  category: 'glasses' | 'robot' | 'toy'
  name: string
  tagline: string
  cover_image: string
}

export interface Feature {
  icon: string
  title: string
  description: string
}

export interface Spec {
  spec_key: string
  spec_value: string
}

export interface ProductImage {
  image_url: string
  alt_text: string
}

export interface ProductDetail extends Product {
  description: string
  features: Feature[]
  specs: Spec[]
  images: ProductImage[]
}

export interface ContactForm {
  name: string
  email: string
  company?: string
  inquiry_type: 'cooperation' | 'media' | 'other'
  message: string
}

export interface Stat {
  label: string
  value: string
  unit: string
}
