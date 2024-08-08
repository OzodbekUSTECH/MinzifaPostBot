from aiogram import types, BaseMiddleware
from typing import Callable, Dict, Any, Awaitable


class AccessMiddleware(BaseMiddleware):
    def __init__(self, allowed_usernames: list):
        self.allowed_usernames = allowed_usernames

    async def __call__(
        self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any]
    ) -> Any:
        current_username = event.from_user.username

        if current_username not in self.allowed_usernames:
            return

        return await handler(event, data)
