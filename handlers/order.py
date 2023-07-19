from config import labeler, api
from vkbottle.bot import Message, rules
from models.models import User, Order
from rules.state_checker import StateChecker
from states.base_state import BaseState
from states.order_states import OrderStates
from keyboards.menu_keyboard import menu_button, three_point, yes_or_no, cancel_button
from messages.order import formed_order, formed_order_to_owner
from random import getrandbits


@labeler.message(StateChecker(OrderStates.ORDER_STATE_GET_LOCATION))
async def get_location(message: Message):
    user = User.get(User.vk_id==message.from_id)
    order = Order.get(user=user)
    order.location = message.text
    if not order.edit_mode:
        user.state = OrderStates.ORDER_STATE_GET_DATETIME
        await message.answer("Напишите дату и время, когда бы Вы хотели провести фотосессию", keyboard=cancel_button)
    else:
        user.state = OrderStates.ORDER_STATE_IS_CORRECT
        await message.answer(formed_order
                    .format(
                        order.location, order.datetime, order.other_info
                    ), keyboard=yes_or_no)
    order.save()
    user.save()

@labeler.message(StateChecker(OrderStates.ORDER_STATE_GET_DATETIME))
async def get_datetime(message: Message):
    user = User.get(User.vk_id==message.from_id)
    order = Order.get(user=user)
    order.datetime = message.text
    if not order.edit_mode:
        user.state = OrderStates.ORDER_STATE_GET_OTHER_INFO
        await message.answer("Ваши ожидания от фотосессии", keyboard=cancel_button)
    else:
        user.state = OrderStates.ORDER_STATE_IS_CORRECT
        await message.answer(formed_order
                    .format(
                        order.location, order.datetime, order.other_info
                    ), keyboard=yes_or_no)
    order.save()
    user.save()

@labeler.message(StateChecker(OrderStates.ORDER_STATE_GET_OTHER_INFO))
async def get_other_info(message: Message):
    user = User.get(User.vk_id==message.from_id)
    order = Order.get(user=user)
    order.other_info = message.text
    user.state = OrderStates.ORDER_STATE_IS_CORRECT
    order.save()
    user.save()
    await message.answer(formed_order
                        .format(
                            order.location, order.datetime, order.other_info
                        ), keyboard=yes_or_no)

@labeler.message(StateChecker(OrderStates.ORDER_STATE_IS_CORRECT))
async def is_odrder_correct(message: Message):
    user: User = User.get(User.vk_id==message.from_id)
    order: Order = Order.get(user=user)
    if message.text == "Да":
        await api.messages.send(172113001, random_id=getrandbits(32), message=formed_order_to_owner.format(
            order.location, order.datetime, order.other_info, user.vk_id
        ))
        await message.answer("Спасибо за заказ, с Вами свяжутся в ближайшее время!", keyboard=menu_button)
        user.state = BaseState.BASE_STATE
        user.save()
        order.delete_instance()
    elif message.text == "Нет":
        await message.answer("Выберите пункт, который хотите исправить", keyboard=three_point)
        user.state = OrderStates.ORDER_STATE_GET_POINT_TO_CHANGE
        user.save()

@labeler.message(StateChecker(OrderStates.ORDER_STATE_GET_POINT_TO_CHANGE))
async def edit_point(message: Message):
    user: User = User.get(User.vk_id==message.from_id)
    order: Order = Order.get(user=user)
    if message.text == "1":
        await message.answer("Где бы Вы хотели провести свою фотоссесию?", keyboard=cancel_button)
        user.state = OrderStates.ORDER_STATE_GET_LOCATION
        order.edit_mode = True
    elif message.text == "2":
        await message.answer("Напишите дату и время, когда бы Вы хотели провести фотосессию?", keyboard=cancel_button)
        user.state = OrderStates.ORDER_STATE_GET_DATETIME
        order.edit_mode = True
    elif message.text == "3":
        await message.answer("Где бы Вы хотели провести свою фотоссесию?", keyboard=cancel_button)
        user.state = OrderStates.ORDER_STATE_GET_OTHER_INFO
        order.edit_mode = True
    user.save()
    order.save()
