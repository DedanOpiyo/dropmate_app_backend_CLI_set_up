import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/dev.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Test log entry.")
