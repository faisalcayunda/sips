from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address


def key_user_or_ip(request: Request) -> str:
    uid = getattr(getattr(request, "state", None), "user_id", None)
    return f"user:{uid}" if uid else f"ip:{get_remote_address(request)}"


limiter = Limiter(key_func=key_user_or_ip, default_limits=["10/second", "200/minute"], storage_uri="memory://")
