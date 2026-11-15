import logging, os

def setup_logging(verbose: bool = False, log_file: str = "logs/latest.log") -> None:
    level = logging.DEBUG if verbose else logging.INFO
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logging.basicConfig(
        level=level,
        format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )