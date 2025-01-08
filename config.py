from loguru import logger


# Setting up logger.
logger.add(
    './logs.log',
    level='DEBUG'
)

EXTENSION_PATH = 'YOUR_PATH'
MM_PASSWORD = 'YOUR_PASSWORD'