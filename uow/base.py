from abc import ABC, abstractmethod
from typing import Any


class BaseUnitOfWork(ABC):
    async def __aenter__(self) -> "BaseUnitOfWork":
        return self

    async def __aexit__(
        self,
        exc_type,
        exc,
        tb,
    ) -> None:
        if exc:
            print(f"Caught exception {exc}")
            await self.rollback()
        else:
            await self.commit()

    @abstractmethod
    async def commit(self) -> Any:  # pragma nocover
        ...

    @abstractmethod
    async def rollback(self) -> Any:  # pragma nocover
        ...
