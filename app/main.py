from fastapi import FastAPI

from app.core.shared.infrastructure.database.database import Base, engine
from app.core.user.api.routes.user_routes import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router, prefix='/users')


@app.get('/')
def read_root():
    return {'message': 'Hello World!'}
