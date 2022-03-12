import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

class ENV_VARS(object):
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    BIFM_URL = os.environ.get("BIFM_URL", "https://bifm.tacohitbox.com/api/bypass?url")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    BOT_USERNAME = os.environ.get("BOT_USERNAME")
    LANGUAGE = os.environ.get("LANGUAGE", "EN")
    AUTH_USER = int(os.environ.get("AUTH_USER", 0))
    MAX_MESSAGE_LENGTH = int(os.environ.get("MAX_MESSAGE_LENGTH", 4096))

Config = ENV_VARS

handler = Config.BOT_USERNAME
class CMD(object):
    START = ["start", f"start@{handler}"]
    ATSN = ["artstation", f"artstation@{handler}"]
    BIFM = ["bifm", f"bifm@{handler}"]
    DPLK = ["droplink", f"droplink@{handler}"]
    GPLK = ["gplink", f"gplink@{handler}"]
    MDIK = ["mdisk", f"mdisk@{handler}"]
    WETR = ["wetransfer", f"wetransfer@{handler}"]
    TEML = ["teml", f"teml@{handler}"]
    RUNF = ["eval", f"eval@{handler}"]
