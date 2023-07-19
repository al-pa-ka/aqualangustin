from vkbottle import Keyboard, Text
from vkbottle.tools.dev.keyboard.color import *

menu_inline = (
    Keyboard(
        inline=True
    )
    .add(Text("Сделать заказ"))
    .add(Text("Отзывы"))
    .row()
    .add(Text("Задать вопрос"))
    .row()
    .add(Text("Часто задаваемые вопросы"))
    #.add(Text("Прочее"))
).get_json()

menu_button = (
    Keyboard(
        inline=False,
        one_time=False
    )
    .add(Text("Меню"))
).get_json()

cancel_button = (
    Keyboard(
        inline=False,
        one_time=False
    )
    .add(Text("Отмена"), KeyboardButtonColor.NEGATIVE)
).get_json()

next_button = (
    Keyboard(
        inline=False,
        one_time=False
    )
    .add(Text("Отмена"), KeyboardButtonColor.NEGATIVE)
    .add(Text("Далее"), KeyboardButtonColor.PRIMARY)
).get_json()

yes_or_no = (
     Keyboard(
        inline=False,
        one_time=True
    )
    .add(Text("Да"), KeyboardButtonColor.POSITIVE)
    .add(Text("Нет"), KeyboardButtonColor.NEGATIVE)
).get_json()

three_point = (
    Keyboard(
        inline=True
    )
    .add(Text("1"))
    .add(Text("2"))
    .add(Text("3"))
)

two_point_and_cancel = (
    Keyboard(
        inline=False,
        one_time=True
    )
    .add(Text("1"))
    .add(Text("2"))
    .row()
    .add(Text("Отмена"), KeyboardButtonColor.NEGATIVE)
)

one_point_or_cancel = (
    Keyboard(
        inline=False,
        one_time=True
    )
    .add(Text("1"))
    .add(Text("Отмена"), KeyboardButtonColor.NEGATIVE)
)