from config import labeler
from vkbottle.bot import Message
from messages.menu import menu_text
from messages.popular_questions import popular_questions_text
from keyboards.menu_keyboard import (
                                        menu_button, menu_inline, 
                                        cancel_button, two_point_and_cancel, 
                                        one_point_or_cancel
                                    )

from models.models import User, Order
from states.base_state import BaseState
from states.order_states import OrderStates
from states.feedback_states import FeedbackStates
from states.question_states import QuestionStates
from rules.state_checker import StateChecker

@labeler.message(text="Отмена")
async def cancel(message: Message):
    user = User.get(vk_id=message.from_id)
    user.state = BaseState.BASE_STATE
    user.offset = 0
    user.save()
    await message.answer("Возвращаемся назад", keyboard=menu_button)
    try:
        order = Order(user=user)
        order.delete_instance()
    except:
        pass

@labeler.message(StateChecker(BaseState.BASE_STATE), text="Меню")
async def menu(message: Message):
    await message.answer(menu_text, keyboard=menu_inline)

@labeler.message(StateChecker(BaseState.BASE_STATE), text="Сделать заказ")
async def create_order(message: Message):
    try:
        user = User.get(User.vk_id==message.from_id)
        user.state = OrderStates.ORDER_STATE_GET_LOCATION
        user.save()
        Order.create(user=user).save()
        await message.answer("Где бы Вы хотели провести свою фотоссесию?", keyboard=cancel_button)
    except Exception as exc:
        await message.answer("Кажется произошла какая-то ошибка, попробуйте еще раз")
        return message.from_id

@labeler.message(StateChecker(BaseState.BASE_STATE), text="Отзывы")
async def feedback(message: Message):
    user = User.get(User.vk_id==message.from_id)
    user.state = FeedbackStates.FEEDBACK_STATE_CHECK
    user.save()
    await message.answer("1. Посмотреть отзывы\n2. Оставить отзыв", keyboard=two_point_and_cancel)

@labeler.message(StateChecker(BaseState.BASE_STATE), text="Задать вопрос")
async def to_ask_question(message: Message):
    user = User.get(vk_id=message.from_id)
    user.state = QuestionStates.QUESTION_STATES
    await message.answer("Задайте Ваш вопрос")
    user.save()

@labeler.message(StateChecker(BaseState.BASE_STATE), text="Прочее")
async def other(message: Message):
    pass

@labeler.message(StateChecker(BaseState.BASE_STATE), text="Часто задаваемые вопросы")
async def popular_questions(message: Message):
    user = User.get(vk_id=message.from_id)
    user.state = QuestionStates.POPULAR_QUESTION_STATE
    await message.answer(popular_questions_text, keyboard=one_point_or_cancel)
    user.save()