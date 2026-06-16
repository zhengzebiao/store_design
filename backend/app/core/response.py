from typing import Any


def success(data: Any = None, **extra: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {"success": True, "data": data}
    payload.update(extra)
    return payload


def failure(error_code: str, error_info: str, details: Any = None) -> dict[str, Any]:
    return {
        "success": False,
        "error_code": error_code,
        "error_info": error_info,
        "details": details or {},
    }
