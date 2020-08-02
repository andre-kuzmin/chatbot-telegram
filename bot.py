import telebot
import re
from time import sleep
import keyboards as kb
import messages as msg
import pandas as pd
import yadisk
import xlrd


y = yadisk.YaDisk(token="AgAAAAAFCrD9AAaFsnHBigAYx0Vyg5V-BjRKiZs")

excel_path_names = './names_bot.xlsx'
excel_path_check_homework = 'https://yadi.sk/d/bG8jJj4-8aiR0Q'
df_names = pd.DataFrame({
    'сhat_id': ['2020'],
    'name': ['test'],
    'username': ['@kuzmin_andre']
                         })

try:
    pd.read_excel(excel_path_names)
except FileNotFoundError:
    writer = pd.ExcelWriter(excel_path_names, engine='xlsxwriter')
    df_names.to_excel(writer, 'names')
    writer.save()
df_names_2 = pd.read_excel(excel_path_names,index_col=0)
print(df_names_2)
bot = telebot.TeleBot('1142583846:AAH23gGM09Kh8HeonxFq6VYAxCRw5xVAqmM')
name_regular = r'[мМ]еня [зЗ]овут .*'
number_check_regular = r'(\d+)\.(\d+)\) (.+)'
name_student = ''
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,msg.start_message_student, reply_markup=kb.keyboard_start)

@bot.message_handler(content_types=['text'])

def get_contact_from(message):
    global df_names_2
    if message.text == 'Хорошо':
        bot.send_message(message.chat.id, 'давай тогда познакомимся?',reply_markup=kb.keyboard_get_name)
    elif message.text == 'давай, как ни как учиться вместе':
        bot.send_message(message.chat.id, 'напиши свое имя в формате : меня зовут ...')

    elif re.match(name_regular, message.text):

        df_check = df_names_2['сhat_id'] == message.chat.id
        print(df_check)


        if (df_check.any()) != True:
            bot.send_message(message.chat.id, 'Рад познакомиться, ' + str(re.findall(name_regular, message.text)[0][11:]))
            bot.send_message(message.chat.id, 'Если ты случайно ошибся в имени, или ты вдруг'
                                              ' сходишь  в паспорный стол и поменяешь его, '
                                              'напиши "поменять имя"', reply_markup=kb.keyboard_change_name)
            df_student = pd.DataFrame({'сhat_id': [message.chat.id],
                                                 'name': [str(re.findall(name_regular, message.text)[0][11:])],
                                        'username': [str(message.from_user.username)]})


            df_names_2 = df_names_2.append(df_student,ignore_index=True)
            writer = pd.ExcelWriter(excel_path_names, engine='xlsxwriter')
            df_names_2.to_excel(writer, 'names')
            writer.save()
            print(df_names_2)






        else:
            index = df_names_2.loc[df_names_2['сhat_id'] == message.chat.id].index[0]
            df_names_2.loc[index,'name'] = str(re.findall(name_regular, message.text)[0][11:])
            df_names_2.loc[index,'username'] = str(message.from_user.username)

            bot.send_message(message.chat.id,'Хорошо,теперь я буду тебя называть так',reply_markup=kb.keyboard_change_name)
            writer = pd.ExcelWriter(excel_path_names, engine='xlsxwriter')
            df_names_2.to_excel(writer,'names')
            writer.save()
            index = 0
            print(df_names_2)





    elif re.match(r'[пП]оменять [иИ]мя', message.text):
        bot.send_message(message.chat.id, 'Напиши свое имя в формате : меня зовут ...')
    elif re.match(r'[вВ]се [оО]кей', message.text):
        bot.send_message(message.chat.id, str(msg.after_register_text))
        # sleep(16)
        bot.send_message(message.chat.id, '...'
                                          '\n'
                                          'Прости за большие сообщения, осталось немного!')
        sleep(2)
        bot.send_message(message.chat.id, str(msg.after_register_text_2), reply_markup=kb.keyboard_after_register)
    elif message.text == 'Так точно, капитан!':
        bot.send_message(message.chat.id, 'Удачи в обучении,если что-то непонятно по техническим вопросам пишите "\help"',reply_markup=kb.keyboard_home_menu)
        bot.register_next_step_handler(message, checking_homework)
    elif message.text == 'Что, собственно говоря, происходит?':
        bot.send_message(message.chat.id, 'Если что-то непонятно, в клавиатуре выбери "\help" или напиши вручную'
                                          'Удачи в обучении!',reply_markup=kb.keyboard_home_menu)
        bot.register_next_step_handler(message, checking_homework)
    elif message.text == 'как меня зовут?':
        bot.send_message(message.chat.id, df_names[df_names['сhat_id'] == message.chat.id]['name'])
    elif message.text == 'тест':
        bot.send_message(message.chat.id, message.chat.id)
        bot.register_next_step_handler(message,checking_homework)
    elif message.text == 'делит':
        indexx = df_names_2.loc[df_names_2['сhat_id'] == message.chat.id].index[0]
        df_names_2 = df_names_2.drop(index=indexx)
        print(df_names_2)
    elif message.text == 'привет':
        bot.send_message(message.chat.id,'привет Андрей')
    else:
        bot.register_next_step_handler(message, checking_homework(message))
        bot.clear_step_handler(message)


def checking_homework(message):
    if re.match(r'[пП]роверить [дД][Зз]', message.text):
        bot.send_message(message.chat.id,
                         'Пиши номер задания в формате : дз.номер) а затем ответ Например, дз под номером 23, а номер задания в этом дз 2 ,ответ 4 , тогда "23.2) 4"')
    elif re.match(number_check_regular,message.text):
        df_сheck_homework = pd.read_excel(y.get_download_link(path='/bot-tables/test_homework.xlsx'),index_col=0,sheet_name=re.search(number_check_regular,message.text).group(1))
        if df_сheck_homework.loc[int(re.search(number_check_regular, message.text).group(2)), 'Ответ'] == str(re.search(number_check_regular,message.text).group(3)):
            bot.send_message(message.chat.id,'задание верное')
            bot.send_message(message.chat.id,df_names_2.loc[df_names_2.loc[df_names_2['сhat_id'] == message.chat.id].index[0],'name'])

        else:
            bot.send_message(message.chat.id, 'задание неверное( Попробуй еще раз, или можешь получить подсказку')











bot.polling()
