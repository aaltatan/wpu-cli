from loguru import logger


def init_logger() -> None:
    logger.remove()
    logger.add(
        "logs/app.log",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} --> {message}",  # noqa: E501
        rotation="2 days",
    )
