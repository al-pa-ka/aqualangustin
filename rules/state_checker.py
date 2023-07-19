from vkbottle.bot import Message

from models.models import User
from vkbottle.dispatch.rules import ABCRule

class StateChecker(ABCRule):
    def __init__(self, state) -> None:
        self.state = state

    async def check(self, event: Message):
        user_state = User.get(User.vk_id == event.from_id).state
        return user_state==self.state



