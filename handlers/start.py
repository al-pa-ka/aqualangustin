from vkbottle.bot import Message
from vkbottle import GroupEventType
from vkbottle_types.events import MessageAllow, MessageDeny

from config import labeler
from keyboards.menu_keyboard import menu_button
from models.models import User


@labeler.message(func=lambda message: message.text in ("Start", "Начать"))
async def start(message: Message):
    await message.answer("Чтобы начать пользоваться ботом напишите \"Меню\" или нажмите на кнопку снизу",
                         keyboard=menu_button)
    
@labeler.raw_event(GroupEventType.MESSAGE_ALLOW, MessageAllow)
async def save_user_in_db(message_allow: MessageAllow):
    try:
        user = User.get(vk_id=message_allow.object.user_id)
        user.messages_allowed = True
        user.save()
        print("User messages_allowed state changed to True!")
    except:
        User.create(vk_id=message_allow.object.user_id, state=0, messages_allowed=True).save()
        print("User saved! from save_user_in_db")

@labeler.raw_event(GroupEventType.MESSAGE_DENY, MessageDeny)
async def change_messages_allowed_state(message_deny: MessageDeny):
    try:
        user = User.get(User.vk_id==message_deny.object.user_id)
        user.messages_allowed = False
        user.save()
        print("User messages_allowed state changed to False!")
    except:
        User.create(vk_id=message_deny.object.user_id, state=0, messages_allowed=False).save()
        print("User saved! from change_messages_allowed_state")
