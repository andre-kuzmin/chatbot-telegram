import telebot

keyboard_start = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_start.row('Хорошо')

button1 = telebot.types.KeyboardButton('Так точно, капитан!')
button2 = telebot.types.KeyboardButton('Что, собственно происходит')


keyboard_after_register = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard_after_register.add(button1)
keyboard_after_register.add(button2)
keyboard_get_name = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_get_name.row('давай, как ни как учиться вместе')

keyboard_change_name = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_change_name.row('все окей','поменять имя')


test_but_1 = telebot.types.KeyboardButton('test1')
test_but_2 = telebot.types.KeyboardButton('test2')
keyboard_home_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_home_menu.add('проверить дз')
keyboard_home_menu.add('задать вопрос по предмету')
keyboard_home_menu.add('\help')
keyboard_home_menu.add('посмотреть свои оценки')
keyboard_tech_help = telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton('ссылка на тех поддержку',url='https://t.me/kuzmin_andre'))

keyboard_check_homework = telebot.types.InlineKeyboardMarkup()
keyboard_think_or_help = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_think_or_help.row('давай подсказку','подумаю ещё!')
keyboard_teacher = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)


