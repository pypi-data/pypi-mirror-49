import os
import logging


_MAIN_DIR = os.path.split(os.path.split(__file__)[0])[0]
_CONFIG_DIR = os.path.join(_MAIN_DIR, "config")

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger("scotusutils")
logger.setLevel(logging.INFO)

handler = logging.FileHandler(os.path.join(_MAIN_DIR, "main_process.log"))
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.info("Loading & Initializing scotus utils...")
