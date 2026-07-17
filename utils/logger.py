import logging
from rich.logging import RichHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("marketingAgent")

def get_logger(name: str):
    return logging.getLogger(f"marketingAgent.{name}")
