from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import ProductImage
from mysite.database.schema import ProductImageInputSchema, ProductImageOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


product_image_router = APIRouter(prefix='/product-image', tags=['Product Image CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_image_router.post('/', response_model=ProductImageOutSchema)
async def create_product_image(image: ProductImageInputSchema, db: Session = Depends(get_db)):
    image_db = ProductImage(**image.dict())
    db.add(image_db)
    db.commit()
    db.refresh(image_db)
    return image_db

@product_image_router.get('/', response_model=List[ProductImageOutSchema])
async def list_product_images(db: Session = Depends(get_db)):
    return db.query(ProductImage).all()

@product_image_router.get('/{image_id}', response_model=ProductImageOutSchema)
async def detail_product_image(image_id: int, db: Session = Depends(get_db)):
    image_db = db.query(ProductImage).filter(ProductImage.id == image_id).one_or_none()
    if not image_db:
        raise HTTPException(detail='Image not found', status_code=404)
    return image_db


@product_image_router.put('/{image_id}/',response_model=dict)
async def update_product_image(image_id: int,image: ProductImageInputSchema,
                          db: Session = Depends(get_db)):
    image_db = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not image_db:
        raise HTTPException(status_code=404, detail='Image not found')

    for image_key, image_value in image.dict().items():
        setattr(image_db, image_key, image_value)

        db.commit()
        db.refresh(image_db)
        return {'message': 'Image updated successfully'}


@product_image_router.delete('/{image_id}/',response_model=dict)
async def delete_product_image(image_id: int, db: Session = Depends(get_db)):
    image_db = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not image_db:
        raise HTTPException(status_code=404, detail='Image not found')

    db.delete(image_db)
    db.commit()
    return {'message': 'Image deleted successfully'}

