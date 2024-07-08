import logging
from datetime import datetime as dt

logger = logging.getLogger(__name__)

logging.basicConfig(filename='log/SentixAI_log.log', level=logging.INFO)


def log(text:str):
    logger.info(f'{dt.now()}: {text}')