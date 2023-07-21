from typing import Any, Callable, Optional

from fastapi import HTTPException

from app.core.logger import log


def HTTP_ERROR(
    code: int, detail: str, callback: Callable | None = None, params: Any = None
):
    if callback:
        log.warning("Handeling error with callback: %s", callback.__name__)
        callback(params)

    raise HTTPException(
        status_code=code,
        detail=detail,
    )
