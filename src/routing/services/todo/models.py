from pydantic import BaseModel


class CreateTodoRequest(BaseModel):
    user_id: int
    task: str


class CreateTodoResponse(BaseModel):
    id: int


class GetTodoResponse(BaseModel):
    id: int
    user_id: int
    task: str
    done: bool


class AllTodosResponse(BaseModel):
    todos: list[GetTodoResponse]


class TodoStatsResponse(BaseModel):
    count: int
