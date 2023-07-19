from random import getrandbits

from vkbottle.bot import Message

from config import api
from config import labeler
from states.feedback_states import FeedbackStates
from states.base_state import BaseState
from rules.state_checker import StateChecker
from models.models import Feedback, User
from keyboards.menu_keyboard import cancel_button, next_button, menu_button, yes_or_no


@labeler.message(StateChecker(state=FeedbackStates.FEEDBACK_STATE_CHECK))
async def get_feedback_choice(message: Message):
    print("in get_feedback_choice")
    user = User.get(vk_id=message.from_id)
    if message.text == "1":
        feedbacks: list[Feedback] = Feedback.select().where((Feedback.is_published)).limit(6)
        if len(feedbacks) > 5:
            for feedback, num in zip(feedbacks, range(5)):
                await message.answer(forward_messages=(feedback.message_id,), keyboard=next_button)
            user.state = FeedbackStates.FEEDBACK_STATE_LOOK
        else:
            for feedback in feedbacks:
                await message.answer(forward_messages=(feedback.message_id,), keyboard=menu_button)
            user.state = BaseState.BASE_STATE
            if len(feedbacks) == 0:
                await message.answer("Отзывов пока нет", keyboard=menu_button)
    elif message.text == "2":
        print("here")
        user.state = FeedbackStates.FEEDBACK_STATE_MAKE_FEEDBACK
        await message.answer("Оставьте свой отзыв", keyboard=cancel_button)
    user.save()
    
@labeler.message(StateChecker(state=FeedbackStates.FEEDBACK_STATE_MAKE_FEEDBACK))
async def make_feedback(message: Message):
    user = User.get(vk_id=message.from_id)
    user.state = FeedbackStates.FEEBACK_EDIT_FEEDBACK
    print("message_id = {}, message_conversation_id = {}, id = {}".format(message.message_id, message.conversation_message_id, message.id))
    feedback = Feedback(message_id=message.id, user=user)
    feedback.save()
    await message.answer("Вот ваш отзыв, всё верно?", keyboard=yes_or_no, forward_messages=(feedback.message_id,))
    user.save()
    

@labeler.message(StateChecker(state=FeedbackStates.FEEBACK_EDIT_FEEDBACK))
async def edit_feedback(message: Message):
    user = User.get(vk_id=message.from_id)
    owner = User.get(vk_id=172113001)
    feedback = Feedback.select().where((Feedback.user==user)).order_by(Feedback.id.desc()).get()
    if message.text == "Да":
        await message.answer("Спасибо за Ваш отзыв!", keyboard=menu_button)
        user.state = BaseState.BASE_STATE
        print("\n\n {}".format(owner.state))
        if owner.state != FeedbackStates.FEEDBACK_STATE_MODERATION:
            await api.messages.send(172113001, random_id=getrandbits(32), forward_messages=(feedback.message_id,), keyboard=yes_or_no)
            print("\n\nIn edit_feedback\n\n")
            owner.state = FeedbackStates.FEEDBACK_STATE_MODERATION
    elif message.text == "Нет":
        user.state = FeedbackStates.FEEDBACK_STATE_MAKE_FEEDBACK
        await message.answer("Оставьте свой отзыв", keyboard=cancel_button)
    user.save()
    owner.save()


@labeler.message(StateChecker(state=FeedbackStates.FEEDBACK_STATE_LOOK))
async def look_feedbacks(message: Message):
    user = User.get(vk_id=message.from_id)
    offset = user.offset if user.offset else 5
    feedbacks: list[Feedback] = Feedback.select().where((Feedback.is_published==True)).order_by(Feedback.id.desc()).limit(5).offset(5)
    if not feedbacks:
        await message.answer("Это всё", keyboard=menu_button)
        user.state = BaseState.BASE_STATE
    elif len(feedbacks) < 5:
        for feedback in feedbacks:
            await api.messages.send(user_id=message.from_id, random_id=getrandbits(64), forward_messages=(feedback.message_id,))
        await message.answer("Это всё", keyboard=menu_button)
        user.state = BaseState.BASE_STATE
    else:
        for feedback in feedbacks:
            await message.answer(forward=feedback.message_id, keyboard=next_button)
        user.offset = offset + 5
    user.save()

@labeler.message(StateChecker(state=FeedbackStates.FEEDBACK_STATE_MODERATION))
async def moderation(message: Message):
    owner = User.get(vk_id=172113001)
    feedbacks = Feedback.select().where((Feedback.on_moderation==True)).order_by(Feedback.id.asc())
    if message.text == "Да":
        feedbacks[0].on_moderation = False
        feedbacks[0].is_published = True
    elif message.text == "Нет":
        feedbacks[0].on_moderation = False
        feedbacks[0].is_published = False
    else:
        await message.answer("Да или нет")
        return
    feedbacks[0].save()
    print("after_save")
    if len(feedbacks) > 1:
        await api.messages.send(owner.vk_id, getrandbits(32), forward_messages=(feedbacks[1].message_id), keyboard=yes_or_no)
    else:
        owner.state = BaseState.BASE_STATE
        await api.messages.send(owner.vk_id, getrandbits(32), message="Это всё")
    owner.save()

