from loguru import logger


def init_logger() -> None:
    logger.remove()
    logger.add(
        "app.log",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} --> {message}",  # noqa: E501
    )
