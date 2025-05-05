from typing import Any

from app import db
from app.models import Category
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)


class CategoryService:
    @staticmethod
    def get_all_categories() -> list[CategoryResponse]:
        categories = Category.query.all()
        return [CategoryResponse.model_validate(cat) for cat in categories]

    @staticmethod
    def get_category_by_id(category_id: int) -> CategoryResponse:
        category = Category.query.get_or_404(category_id)
        return CategoryResponse.model_validate(category)

    @staticmethod
    def create_category(data: dict[str, Any]) -> CategoryResponse:
        try:
            category_data = CategoryCreate(**data)
            category = Category(**category_data.model_dump())
            db.session.add(category)
            db.session.commit()
            return CategoryResponse.model_validate(category)
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e)) from e

    @staticmethod
    def update_category(category_id: int, data: dict[str, Any]) -> CategoryResponse:
        try:
            category = Category.query.get_or_404(category_id)
            category_data = CategoryUpdate(**data)

            for field, value in category_data.model_dump(exclude_unset=True).items():
                setattr(category, field, value)

            db.session.commit()
            return CategoryResponse.model_validate(category)
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e)) from e

    @staticmethod
    def delete_category(category_id: int) -> dict[str, Any]:
        try:
            category = Category.query.get_or_404(category_id)
            db.session.delete(category)
            db.session.commit()
            return {"message": "Category deleted successfully"}
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e)) from e
