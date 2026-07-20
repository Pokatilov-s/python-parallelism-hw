import uuid
from typing import Callable

import asyncio
from src.domain.report import Report, Todo, TodoList, User
from src.infrastructure.clients.dummyjson_client import DummyJsonClient
from src.infrastructure.job_store import JobStore


class ReportService:

    def __init__(
            self,
            user_client: DummyJsonClient,
            todos_client: Callable[[int], dict],
    ):
        self._user_client = user_client
        self._todo_sync_client = todos_client

    async def get_todos(self, user_id) -> TodoList:
        res = await asyncio.to_thread(self._todo_sync_client, user_id)
        todos = [Todo(id=t["id"], todo=t["todo"], completed=t["completed"]) for t in res["todos"]]
        return TodoList(
            total=res["total"],
            completed=sum([1 for t in todos if t.completed]),
            items=todos,
        )

    async def get_user(self, user_id: int) -> User:
        res = await self._user_client.get_user(user_id)
        return User(
            user_id=res.id,
            user_name=f"{res.first_name} {res.last_name}",
            email=res.email,
        )

    async def build_report(self, user_id) -> Report:
        async with asyncio.TaskGroup() as tg:
            task_user: asyncio.Task = tg.create_task(self.get_user(user_id))
            task_todos: asyncio.Task = tg.create_task(self.get_todos(user_id))

        return Report(
            user=task_user.result(),
            todos=task_todos.result(),
        )









