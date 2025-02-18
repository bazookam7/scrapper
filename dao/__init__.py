import os
from dotenv import load_dotenv
import logging
load_dotenv(os.path.join(os.path.curdir,"set_paths.env"))

logging.info("DAO initialized")