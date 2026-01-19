from loguru import logger


def init_logger() -> None:
    logger.add(
        "logs/app.log",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} --> {message}",
        rotation="2 days",
    )
