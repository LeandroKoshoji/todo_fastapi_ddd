from fastapi import FastAPI

from app.core.shared.infrastructure.database.database import Base, engine
from app.core.task.api.routes.task_routes import router as task_router
from app.core.user.api.routes.user_routes import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router, tags=['auth'])
app.include_router(task_router, prefix='/tasks', tags=['tasks'])


@app.get('/')
def read_root():
    return {'message': 'Hello World!'}
