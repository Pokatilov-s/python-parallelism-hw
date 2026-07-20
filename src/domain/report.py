from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    user_name: str
    email: str


@dataclass
class Todo:
    id: int
    todo: str
    completed: bool


@dataclass
class TodoList:
    total: int
    completed: int
    items: list[Todo]


@dataclass
class Report:
    user: User
    todos: TodoList
