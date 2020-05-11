import logging

logger = logging.getLogger(__name__)

# Create handlers

# Dictates all the words to the script log
# INFO level

stenographer = logging.FileHandler('script.log')
stenographer.setLevel(logging.ERROR)
stenographer_format = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
stenographer.setFormatter(stenographer_format)
logger.addHandler(stenographer)
logger.error("This is a test")
