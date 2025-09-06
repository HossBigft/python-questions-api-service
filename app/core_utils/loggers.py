import logging

from datetime import datetime, timedelta
from starlette.middleware.base import BaseHTTPMiddleware




from fastapi import Request



USER_ACTION_LOG_SIZE_MB = 10


def round_up_seconds(dt: datetime):
    if dt.microsecond > 0:
        return (dt + timedelta(seconds=1)).replace(microsecond=0)
    return dt.replace(microsecond=0)


def _get_timestamp() -> str:
    now = datetime.now()
    rounded_time = round_up_seconds(now)
    return rounded_time.isoformat()


class CompactDockerFormatter(logging.Formatter):
    def format(self, record):
        timestamp = _get_timestamp()

        message = record.getMessage()
        client = "-"
        request_line = "-"
        status_code = "-"
        duration_ms = getattr(record, "duration_ms", None)

        try:
            parts = message.split(" - ")
            client = parts[0]
            request_info = parts[1].strip("'")
            request_line, status_code = request_info.rsplit(" ", 1)
        except Exception:
            pass

        time_str = f"{duration_ms:.2f}ms" if duration_ms is not None else "-"

        return (
            f"{timestamp} level={record.levelname} "
            f'client={client} status={status_code} req="{request_line}" time={time_str}'
        )


def disable_default_uvicorn_access_logs():
    logger = logging.getLogger("uvicorn.access")
    logger.handlers.clear()


def setup_custom_access_logger():
    logger = logging.getLogger("app.access")
    handler = logging.StreamHandler()
    logger.propagate = False
    handler.setFormatter(CompactDockerFormatter())
    logger.addHandler(handler)
    return logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        real_ip = _get_request_ip(request)

        start = datetime.now()
        response = await call_next(request)
        duration = (datetime.now() - start).total_seconds() * 1000  # in ms

        request_line = f"{request.method} {request.url.path} HTTP/{request.scope.get('http_version', '1.1')}"
        logger = logging.getLogger("app.access")
        logger.info(
            f"{real_ip} - '{request_line} {response.status_code}'",
            extra={"duration_ms": duration},
        )

        return response


def _mb_to_bytes(mb: int) -> int:
    return mb * 1024 * 1024


def _get_request_ip(request: Request) -> str:
    ip: str
    try:
        ip = request.headers["X-Forwarded-For"]
    except KeyError:
        ip = request.client.host
    return ip


