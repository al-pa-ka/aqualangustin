from vkbottle import API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler
import logging

api: API = API("TOKEN")
labeler = BotLabeler()
pewee_logger = logging.getLogger("peewee")
pewee_logger.disabled = True
