from fastapi import Request


async def authenticate_user_middleware(request: Request, call_next): ...
