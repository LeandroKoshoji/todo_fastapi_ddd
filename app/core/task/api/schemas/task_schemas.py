from pydantic import BaseModel

from app.core.task.domain.task import TaskStatus


class TaskBaseModel(BaseModel):
    title: str
    status: TaskStatus
    description: str
    send_notification: bool


class TaskResponseBaseModel(TaskBaseModel):
    id: str
    user_id: str
    created_at: str
    updated_at: str


class CreateTaskSchema(TaskBaseModel):
    pass


class CreateTaskResponseModel(TaskResponseBaseModel):
    pass


class EditTaskSchema(TaskBaseModel):
    pass


class EditTaskResponseModel(TaskResponseBaseModel):
    pass


class ListTaskByIdResponseModel(TaskResponseBaseModel):
    pass
