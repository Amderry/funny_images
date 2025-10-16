import logging

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(pathname)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger()
