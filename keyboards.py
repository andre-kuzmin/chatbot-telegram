import telebot
import yadisk

y = yadisk.YaDisk(token="AgAAAAAFCrD9AAaFsnHBigAYx0Vyg5V-BjRKiZs")
# start
keyboard_start = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_start.row('Хорошо')
keyboard_start_understand  = telebot.types.InlineKeyboardMarkup()
# https://yadi.sk/i/FXjhKGraNu9Reg
keyboard_start_understand.add(telebot.types.InlineKeyboardButton(text='смотреть видео',url = 'https://yadi.sk/i/FXjhKGraNu9Reg'))
keyboard_start_understand.add(telebot.types.InlineKeyboardButton(text='открыть pdf файл',url = 'https://yadi.sk/i/LpdztBfw4DVrOQ'))

# y.get_download_link(path='/start/test_homework.xlsx')

# get contact
button1 = telebot.types.KeyboardButton('Так точно, капитан!')
button2 = telebot.types.KeyboardButton('Что, собственно говоря, происходит?')


keyboard_after_register = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard_after_register.add(button1)
keyboard_after_register.add(button2)
keyboard_get_name = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_get_name.row('давай, как ни как учиться вместе')

keyboard_change_name = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_change_name.row('все окей','поменять имя')




# home menu
keyboard_home_menu = telebot.types.ReplyKeyboardMarkup()
keyboard_home_menu.add('проверить дз')
keyboard_home_menu.add('задать вопрос по предмету')
keyboard_home_menu.add('техническая поддержка')
keyboard_home_menu.add('посмотреть свои оценки')


# tech helping

keyboard_tech_help = telebot.types.InlineKeyboardMarkup()
keyboard_tech_help.add(telebot.types.InlineKeyboardButton('ссылка на тех поддержку',url='https://t.me/kuzmin_andre'))

# ask quection about subject
keyboard_subject_help = telebot.types.InlineKeyboardMarkup()
keyboard_subject_help.add(telebot.types.InlineKeyboardButton('ссылка вопросы по предмету',url='https://t.me/NikVarf'))



# getting answers and helping
keyboard_think_or_help = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_think_or_help.row('давай подсказку','подумаю ещё!')
keyboard_teacher = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_after_reshenie = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_after_reshenie.add('теперь разобрался!')
keyboard_after_reshenie.add('все равно не понял, остались вопросы')

