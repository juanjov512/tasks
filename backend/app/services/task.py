from typing import Any

from app import db
from app.models import Label, Task
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


class TaskService:
    @staticmethod
    def get_user_tasks(user_id: int) -> list[TaskResponse]:
        tasks = Task.query.filter_by(user_id=user_id).all()
        return [TaskResponse.model_validate(task) for task in tasks]

    @staticmethod
    def get_task(task_id: int, user_id: int) -> TaskResponse:
        task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
        return TaskResponse.model_validate(task)

    @staticmethod
    def create_task(user_id: int, data: dict[str, Any]) -> TaskResponse:
        try:
            task_data = TaskCreate(**data)
            task = Task(
                user_id=user_id,
                title=task_data.title,
                content=task_data.content,
                due_date=task_data.due_date,
                status=task_data.status,
                priority=task_data.priority,
                category_id=task_data.category_id,
            )

            if task_data.labels:
                labels = Label.query.filter(Label.id.in_(task_data.labels)).all()
                task.labels = labels

            db.session.add(task)
            db.session.commit()

            return TaskResponse.model_validate(task)
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e)) from e

    @staticmethod
    def update_task(task_id: int, user_id: int, data: dict[str, Any]) -> TaskResponse:
        try:
            task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()

            update_data = TaskUpdate(**data)
            for field, value in update_data.model_dump(exclude_unset=True).items():
                if field == "labels" and value is not None:
                    labels = Label.query.filter(Label.id.in_(value)).all()
                    task.labels = labels
                else:
                    setattr(task, field, value)

            db.session.commit()
            return TaskResponse.model_validate(task)
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e)) from e

    @staticmethod
    def delete_task(task_id: int, user_id: int) -> dict[str, Any]:
        try:
            task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
            db.session.delete(task)
            db.session.commit()
            return {"message": "Task deleted successfully"}
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e)) from e

    @staticmethod
    def add_labels_to_task(task_id: int, user_id: int, label_ids: list[int]) -> dict[str, Any]:
        try:
            task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()

            if not label_ids:
                raise ValueError("Labels IDs are required")

            labels = Label.query.filter(Label.id.in_(label_ids)).all()
            task.labels.extend(labels)

            db.session.commit()
            return {"message": "Labels added successfully"}
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e)) from e

    @staticmethod
    def remove_label_from_task(task_id: int, user_id: int, label_id: int) -> dict[str, Any]:
        try:
            task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
            label = Label.query.get_or_404(label_id)

            if label not in task.labels:
                raise ValueError("Label is not associated with this task")

            task.labels.remove(label)
            db.session.commit()
            return {"message": "Label removed successfully"}
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e)) from e
