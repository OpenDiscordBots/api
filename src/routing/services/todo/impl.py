from fastapi import APIRouter, HTTPException
from fastapi.routing import APIRoute
from ormar import NoMatch

from src.impl.database import Todo, get_user

from .models import (
    AllTodosResponse,
    CreateTodoRequest,
    CreateTodoResponse,
    GetTodoResponse,
    TodoStatsResponse,
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

    return GetTodoResponse(id=todo.id, user_id=todo.user.id, task=todo.task, done=todo.done)


@router.patch("/{id}", response_model=GetTodoResponse)
async def update_todo(id: int, done: bool) -> GetTodoResponse:
    """Update the completion status of a Todo task."""

    try:
        todo = await Todo.objects.first(id=id)
    except NoMatch:
        raise HTTPException(404, "Task not found")

    todo = await todo.update(done=done)

    return GetTodoResponse(id=todo.id, user_id=todo.user.id, task=todo.task, done=todo.done)


@router.delete("/{id}", status_code=204)
async def delete_todo(id: int) -> None:
    """Delete a Todo task."""

    try:
        todo = await Todo.objects.first(id=id)
    except NoMatch:
        raise HTTPException(404, "Task not found")

    await todo.delete()


@router.get("/all/{user_id}", response_model=AllTodosResponse)
async def get_all_todos(user_id: int, include_done: bool = False) -> AllTodosResponse:
    """Get all Todo tasks for a given user."""

    user = await get_user(user_id)

    if include_done:
        todos = await Todo.objects.filter(user=user.id).all()
    else:
        todos = await Todo.objects.filter(user=user.id, done=False).all()

    return AllTodosResponse(
        todos=[GetTodoResponse(id=todo.id, user_id=todo.user.id, task=todo.task, done=todo.done) for todo in todos]
    )


@router.get("/stats/all", response_model=TodoStatsResponse)
async def get_todo_stats() -> TodoStatsResponse:
    """Get stats for the Todo service."""

    count = await Todo.objects.count()

    return TodoStatsResponse(count=count)
