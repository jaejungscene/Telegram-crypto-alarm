import argparse

from bot.io_client import UserConfiguration
from bot.custom_logger import logger

parser = argparse.ArgumentParser()
parser.add_argument('--id', type=str, required=True,
                    help='See how to get your TG user ID here: https://www.youtube.com/watch?v=W8ifn3ATpdA')

# Parse the argument
args = parser.parse_args()
user_id = args.id

# Set up required user files:
try:
    logger.info(f"Creating default bot configuration for Telegram user {user_id}...")

    UserConfiguration(user_id).whitelist_user(is_admin=True)

    logger.info("Setup complete! You can now run the bot module using: python3 -m bot")
except Exception as exc:
    logger.exception("An unexpected error occurred during setup", exc_info=exc)
