from pydantic import BaseModel
from typing import Generic, TypeVar, Any

DataT = TypeVar('DataT', bound=Any)


class BaseResponse(BaseModel, Generic[DataT]):
    message: str | None = None
    data: DataT | None = None
    error: str | None = None
    success: bool = True

    @staticmethod
    def ok(data: DataT, message: str):
        return BaseResponse[DataT](data=data, message=message)

    @staticmethod
    def fail(error: str, message: str):
        return BaseResponse[DataT](error=error, message=message, success=False)
