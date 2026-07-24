import httpx
from pydantic import BaseModel, Field


class DummyJsonUser(BaseModel):
    id: int
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    email: str


class DummyJsonClient:
    _BASE_URL = "https://dummyjson.com"

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(base_url= self._BASE_URL)

    async def _get(self, path: str, params: dict | None = None) -> httpx.Response:
        res = await self._client.get(path, params=params)
        res.raise_for_status()
        return res

    async def get_user(self, user_id: int) -> DummyJsonUser:
        res = await self._get(path=f"users/{user_id}")
        return DummyJsonUser.model_validate_json(res.content)

    async def aclose(self) -> None:
        await self._client.aclose()
