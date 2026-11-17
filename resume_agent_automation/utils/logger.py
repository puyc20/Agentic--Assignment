import logging
from pathlib import Path

from resume_agent_automation.config.settings import PATHS


def get_logger(name: str, log_file: str | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if log_file:
            file_path = Path(log_file)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(file_path)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        else:
            file_path = PATHS.logs_dir / f"{name}.log"
            file_handler = logging.FileHandler(file_path)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger
