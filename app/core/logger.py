import logging

from uvicorn.logging import ColourizedFormatter

from app.core.settings import env

log = logging.getLogger()

log.setLevel(env.app_log_level)

console_handler = logging.StreamHandler()
console_handler.setFormatter(
    ColourizedFormatter("%(levelprefix)s %(asctime)s | %(message)s")
)

log.addHandler(console_handler)
