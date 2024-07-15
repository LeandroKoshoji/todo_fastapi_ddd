# Todo Application + FastAPI + DDD + Clean Architecture

## How to Run the Project

### Prerequisites

Make sure you have Docker and Docker Compose installed and running on your machine.

### Setup

1. Clone the repository.
2. Rename the `.env.example` file to `.env`.

### Running in Development

To start the application in development mode, navigate to the root directory of the project and run the following command:

```bash
docker-compose -f docker-compose.dev.yml up --build
```

> The application will be accessible at http://localhost:8000

> Swagger at http://localhost:8000/docs#/default

### Running Integration Tests

To run the integration tests, navigate to the root directory of the project and use the following command:

```bash
docker-compose -f docker-compose.test-integration.yml up --build
```

This will set up the necessary environment and execute the integration tests.

### Project structure

```plaintext
.
├── Dockerfile
├── alembic.ini
├── app
│   ├── config
│   │   └── settings.py
│   ├── core
│   │   ├── shared
│   │   │   ├── application
│   │   │   │   ├── schemas
│   │   │   │   │   └── response.py
│   │   │   │   └── utils.py
│   │   │   ├── domain
│   │   │   │   └── entity.py
│   │   │   ├── infra
│   │   │   │   └── database
│   │   │   │       └── database.py
│   │   │   └── security
│   │   │       ├── dependecies.py
│   │   │       ├── interfaces.py
│   │   │       ├── jwt.py
│   │   │       └── password_hasher.py
│   │   ├── task
│   │   │   ├── api
│   │   │   │   ├── routes
│   │   │   │   │   └── task_routes.py
│   │   │   │   └── schemas
│   │   │   │       └── task_schemas.py
│   │   │   ├── application
│   │   │   │   ├── factories
│   │   │   │   │   └── task_use_case_factory.py
│   │   │   │   └── use_cases
│   │   │   │       ├── create_task_use_case.py
│   │   │   │       ├── delete_task_use_case.py
│   │   │   │       ├── edit_task_use_case.py
│   │   │   │       ├── list_all_tasks_by_user_use_case.py
│   │   │   │       ├── list_task_by_id_use_case.py
│   │   │   │       └── search_tasks_use_case.py
│   │   │   ├── domain
│   │   │   │   ├── commands
│   │   │   │   │   ├── create_task_command.py
│   │   │   │   │   ├── delete_task_command.py
│   │   │   │   │   └── edit_task_command.py
│   │   │   │   ├── events
│   │   │   │   │   ├── task_created_event.py
│   │   │   │   │   ├── task_deleted_event.py
│   │   │   │   │   └── task_edited_event.py
│   │   │   │   ├── exceptions.py
│   │   │   │   ├── task.py
│   │   │   │   └── task_repository.py
│   │   │   └── infra
│   │   │       ├── models
│   │   │       │   └── task_model.py
│   │   │       └── repositories
│   │   │           └── sqlalchemy_task_repository.py
│   │   └── user
│   │       ├── api
│   │       │   ├── routes
│   │       │   │   └── user_routes.py
│   │       │   └── schemas
│   │       │       └── user_schemas.py
│   │       ├── application
│   │       │   ├── factories
│   │       │   │   └── use_case_factory.py
│   │       │   └── use_cases
│   │       │       ├── create_user_use_case.py
│   │       │       └── login_user_use_case.py
│   │       ├── domain
│   │       │   ├── commands
│   │       │   │   ├── create_user_command.py
│   │       │   │   └── login_user_command.py
│   │       │   ├── events
│   │       │   │   ├── user_created_event.py
│   │       │   │   └── user_loggedin_event.py
│   │       │   ├── exceptions.py
│   │       │   ├── user.py
│   │       │   └── user_repository.py
│   │       └── infra
│   │           ├── models
│   │           │   └── user_model.py
│   │           └── repositories
│   │               └── sqlalchemy_user_repository.py
│   └── main.py
├── docker-compose.dev.yml
├── docker-compose.test-integration.yml
├── migrations
├── poetry.lock
├── post.md
├── pyproject.toml
└── tests
    ├── conftest.py
    ├── helpers.py
    ├── integration
    │   └── core
    │       ├── task
    │       │   ├── api
    │       │   │   └── test_task_routes.py
    │       │   └── infra
    │       │       └── repositories
    │       │           └── test_sqlalchemy_task_repository.py
    │       └── user
    │           ├── api
    │           │   └── routes
    │           │       └── test_user_routes.py
    │           └── infra
    │               └── repositories
    │                   └── test_sqlalchemy_user_repository.py
    └── root_test.py
```
