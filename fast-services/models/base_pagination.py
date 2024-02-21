from pydantic import BaseModel
from typing import Generic, TypeVar, Any

DataT = TypeVar('DataT', bound=Any)


class BasePagination(BaseModel, Generic[DataT]):
    results: list[DataT] | None = None
    pagination: dict | None = None

    @staticmethod
    def init(results: list[DataT], total: int = 0, page: int = 0, size: int = 0):
        return BasePagination[DataT](results=results, pagination=dict(total=total, page=page, size=size))
