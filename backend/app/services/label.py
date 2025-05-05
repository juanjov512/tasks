from typing import Any

from app import db
from app.models import Label
from app.schemas.label import LabelCreate, LabelResponse, LabelUpdate


class LabelService:
    @staticmethod
    def get_user_labels(user_id: int) -> list[LabelResponse]:
        labels = Label.query.filter_by(user_id=user_id).all()
        return [LabelResponse.model_validate(label) for label in labels]

    @staticmethod
    def get_label_by_id(label_id: int, user_id: int) -> LabelResponse:
        label = Label.query.filter_by(id=label_id, user_id=user_id).first_or_404()
        return LabelResponse.model_validate(label)

    @staticmethod
    def create_label(user_id: int, data: dict[str, Any]) -> LabelResponse:
        try:
            label_data = LabelCreate(**data)
            label = Label(user_id=user_id, **label_data.model_dump())
            db.session.add(label)
            db.session.commit()
            return LabelResponse.model_validate(label)
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e)) from e

    @staticmethod
    def update_label(label_id: int, user_id: int, data: dict[str, Any]) -> LabelResponse:
        try:
            label = Label.query.filter_by(id=label_id, user_id=user_id).first_or_404()
            label_data = LabelUpdate(**data)

            for field, value in label_data.model_dump(exclude_unset=True).items():
                setattr(label, field, value)

            db.session.commit()
            return LabelResponse.model_validate(label)
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e)) from e

    @staticmethod
    def delete_label(label_id: int, user_id: int) -> dict[str, Any]:
        try:
            label = Label.query.filter_by(id=label_id, user_id=user_id).first_or_404()
            db.session.delete(label)
            db.session.commit()
            return {"message": "Label deleted successfully"}
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e)) from e
