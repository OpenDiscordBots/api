from fastapi import APIRouter, HTTPException
from ormar import NoMatch

from src.impl.database import Todo, get_user

from .models import (
    CreateTodoRequest,
    CreateTodoResponse,
    GetTodoResponse,
    TodoStatsResponse,
    UserTodosResponse,
)

router = APIRouter(prefix="/todo", tags=["Todo"])


@router.post("/", response_model=CreateTodoResponse)
async def create_todo(request: CreateTodoRequest) -> CreateTodoResponse:
    """Create a new Todo task."""

    user = await get_user(request.user_id, strict=True)

    todo = await Todo(user=user, task=request.task).save()

    return CreateTodoResponse(id=todo.id)


@router.get("/{id}", response_model=GetTodoResponse)
async def get_todo(id: int) -> GetTodoResponse:
    """Get an existing Todo task."""

    try:
        todo = await Todo.objects.first(id=id)
    except NoMatch:
        raise HTTPException(404, "Task not found")

    return GetTodoResponse(id=todo.id, user_id=todo.user.id, task=todo.task, done=todo.done, namespace=todo.namespace)


@router.patch("/{id}", response_model=GetTodoResponse)
async def update_todo(id: int, done: bool = None, namespace: str = None) -> GetTodoResponse:
    """Update the completion status of a Todo task."""

    if done is None and namespace is None:
        raise HTTPException(422, "No update parameters provided")

    try:
        todo = await Todo.objects.first(id=id)
    except NoMatch:
        raise HTTPException(404, "Task not found")

    kwargs = {}
    if done is not None:
        kwargs["done"] = done
    if namespace is not None:
        kwargs["namespace"] = namespace

    todo = await todo.update(**kwargs)

    return GetTodoResponse(id=todo.id, user_id=todo.user.id, task=todo.task, done=todo.done, namespace=todo.namespace)


@router.delete("/{id}", status_code=204)
async def delete_todo(id: int) -> None:
    """Delete a Todo task."""

    try:
        todo = await Todo.objects.first(id=id)
    except NoMatch:
        raise HTTPException(404, "Task not found")

    await todo.delete()


@router.get("/users/{user_id}", response_model=UserTodosResponse)
async def get_user_todos(user_id: int, include_done: bool = False) -> UserTodosResponse:
    """Get all Todo tasks for a given user."""

    user = await get_user(user_id)

    if include_done:
        todos = await Todo.objects.filter(user=user.id).all()
    else:
        todos = await Todo.objects.filter(user=user.id, done=False).all()

    return UserTodosResponse(
        todos=[
            GetTodoResponse(id=todo.id, user_id=todo.user.id, task=todo.task, done=todo.done, namespace=todo.namespace)
            for todo in todos
        ]
    )


@router.get("/stats/all", response_model=TodoStatsResponse)
async def get_todo_stats() -> TodoStatsResponse:
    """Get stats for the Todo service."""

    count = await Todo.objects.count()

    return TodoStatsResponse(count=count)
