from vkbottle import Bot

import handlers
from config import labeler, api



bot = Bot(api=api, labeler=labeler
        ).run_forever()