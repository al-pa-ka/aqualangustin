from vkbottle.bot import Message
from random import getrandbits

from rules.state_checker import StateChecker
from config import labeler
from config import api
from states.base_state import BaseState
from states.question_states import QuestionStates
from keyboards.menu_keyboard import menu_button
from models.models import User


@labeler.message(StateChecker(state=QuestionStates.QUESTION_STATES))
async def ask_question(message: Message):
    user = User.get(vk_id=message.from_id)
    await api.messages.send(172113001, random_id=getrandbits(64), forward_messages=(message.id,))
    await message.answer("Вам скоро ответят", keyboard=menu_button)
    user.state = BaseState.BASE_STATE
    user.save()

