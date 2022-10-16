import dotenv
import logging
import logging.handlers
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler(
            filename="./log.txt",
            mode='w'
        ),
        logging.StreamHandler(sys.stdout)
    ],
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

authorized_chats = ["-1001751748596", "1485677797", "-1001786055055"]
filenames = {}

dotenv.load_dotenv("config.env")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID", "12345"))
API_HASH = os.environ.get("API_HASH")