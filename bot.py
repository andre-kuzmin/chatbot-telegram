import telebot
import re
from time import sleep
import keyboards as kb
import messages as msg
import pandas as pd
import yadisk
from PIL import Image
from urllib.request import urlopen
import xlrd
# поменял
# поменял 2
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
bot = telebot.TeleBot('1287969362:AAFGI-capLkHpSN3QbrwSgZ-NcxzEzFlALc')
name_regular = r'[мМ]еня [зЗ]овут .*'
number_check_regular = r'(\d+)\.(\d+)\) (.+)'
get_podskaska_regular = r'((\d+)\.(\d+))\) (.+)'
get_reshenie_regular = r'((\d+)\.(\d+))\) [Рр]ешение'

get_podskaska_regular_2 = r'((\d+)\.(\d+))\.(.+)'
format_image_regular = r'\.(.+)'
name_student = ''

# @bot.callback_query_handler(func=lambda call:True)
# def helping(call):
#
#     if  call.data == '1':
#         bot.answer_callback_query(callback_query_id=call.id, text='Напиши любой вопрос сюда:')
@bot.message_handler(commands=['start'])
def start_message(message):

    bot.send_message(message.chat.id,msg.start_message_student, reply_markup=kb.keyboard_start)
    sleep(1)
    bot.send_message(message.chat.id,'А и еще, я скидываю тебе видео и pdf файл с обьяснением, как работает бот\n'
                                     'Я уверен, что ты бы мог сходу разобраться, но посмотреть лишним не будет!',reply_markup=kb.keyboard_start_understand)
    sleep(2)
    bot.send_message(message.chat.id,'Если пока все понятно , нажми на клавиатуре хорошо, если же уже появились вопросы, напиши или нажми на  /help', reply_markup=kb.keyboard_start)
@bot.message_handler(commands=['help'])
def help_tech(message):
    bot.send_message(message.chat.id,'по всем техническим вопросам пиши сюда',reply_markup = kb.keyboard_tech_help)
@bot.message_handler(content_types=['text'])

def get_contact_from(message):
    global df_names_2
    if str(message.from_user.username) == 'NikVarf':
        bot.send_message(message.chat.id,'Добрый день, мой Господин-преподаватель! Для вас есть специальные функции, предложенные в клавиатуре. Удачной работы, Господин!')
    if message.text == 'Хорошо':
        bot.send_message(message.chat.id, 'давай тогда познакомимся?',reply_markup=kb.keyboard_get_name)
    elif message.text == 'давай, как ни как учиться вместе':
        bot.send_message(message.chat.id, 'напиши свое имя в формате : меня зовут ...')

    elif re.match(name_regular, message.text):

        df_check = df_names_2['сhat_id'] == message.chat.id


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






        else:
            index = df_names_2.loc[df_names_2['сhat_id'] == message.chat.id].index[0]
            df_names_2.loc[index,'name'] = str(re.findall(name_regular, message.text)[0][11:])
            df_names_2.loc[index,'username'] = str(message.from_user.username)

            bot.send_message(message.chat.id,'Хорошо,теперь я буду тебя называть так',reply_markup=kb.keyboard_change_name)
            writer = pd.ExcelWriter(excel_path_names, engine='xlsxwriter')
            df_names_2.to_excel(writer,'names')
            writer.save()
            index = 0





    elif re.match(r'[пП]оменять [иИ]мя', message.text):
        bot.send_message(message.chat.id, 'Напиши свое имя в формате : меня зовут ...')
    elif re.match(r'[вВ]се [оО]кей', message.text):

        bot.send_message(message.chat.id, 'Надеюсь ,что ты все понял, так что могу только пожелать удачи! готов начать обучение?', reply_markup=kb.keyboard_after_register)
    elif message.text == 'Так точно, капитан!':
        bot.send_message(message.chat.id, 'Удачи в обучении,если что-то непонятно по техническим вопросам напиши или нажми на "/help" ',reply_markup=kb.keyboard_home_menu)
        bot.register_next_step_handler(message, checking_homework)
    elif message.text == 'Что, собственно говоря, происходит?':
        bot.send_message(message.chat.id, 'Если что-то непонятно, нажми на /help или напиши вручную. Так же , по любым техническим вопросам можешь выбрать в клавиатуре "техническая поддержка" '
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
    elif message.text == '/help':
        bot.send_message(message.chat.id, 'По всем техническам вопросам пиши сюда!', reply_markup=kb.keyboard_tech_help)

    else:

        bot.register_next_step_handler(message, checking_homework(message))
        bot.clear_step_handler(message)

#Проверка дз
def checking_homework(message):

    if re.match(r'[пП]роверить [дД][Зз]', message.text):
        bot.send_message(message.chat.id,
                         'Пиши номер задания в формате : дз.номер) а затем ответ Например, дз под номером 23, а номер задания в этом дз 2 ,ответ 4 , тогда "23.2) 4"')
    elif re.match(number_check_regular,message.text):
        if re.match(r'[пП]одсказка', str(re.search(number_check_regular, message.text).group(3))) == None:
            df_check_homework = pd.read_excel(y.get_download_link(path='/bot-tables/test_homework.xlsx'),index_col=0,sheet_name=re.search(number_check_regular,message.text).group(1),converters={'Ответ': str})
            if df_check_homework.loc[int(re.search(number_check_regular, message.text).group(2)), 'Ответ'] == str(re.search(number_check_regular,message.text).group(3)):
                bot.send_message(message.chat.id,'задание верное')
                bot.send_message(message.chat.id,df_names_2.loc[df_names_2.loc[df_names_2['сhat_id'] == message.chat.id].index[0],'name']+',ты молодец!',reply_markup=kb.keyboard_home_menu)
            else:
                bot.send_message(message.chat.id, 'задание неверное(')
                bot.send_message(message.chat.id,df_names_2.loc[df_names_2.loc[df_names_2['сhat_id'] == message.chat.id].index[0],'name']+', подумаешь еще или хочешь получить подсказку?',reply_markup=kb.keyboard_think_or_help)
        else:
            bot.send_photo(message.chat.id,photo=y.get_download_link(path='/podskaski/'+str(re.search(get_podskaska_regular,message.text).group(1))+'.jpg'),
                           caption='держи подсказку к заданию №'+str(re.search(get_podskaska_regular,message.text).group(1)),reply_markup=kb.keyboard_home_menu)

    elif re.match(r'[Дд]авай [пП]одсказку', message.text):

        bot.send_message(message.chat.id, 'напиши в формате : "дз.номер из дз) подсказка".\n'
                                          ' К примеру : дз номер 2, номер из домашнего задания 4, тогда 2.4) подсказка')
    elif re.match(r'[Дд]авай [рР]ешение', message.text):

        bot.send_message(message.chat.id, 'напиши в формате : "дз.номер из дз) решение".\n'
                                          ' К примеру : дз номер 2, номер из домашнего задания 4, тогда 2.4) решение')

    elif re.match(r'[пП]одумаю [еЕ]щё!',message.text):
        bot.send_message(message.chat.id,'Хорошо, так держать!',reply_markup=kb.keyboard_home_menu)
#     просмотр оценок

    elif re.match(r'[Пп]осмотреть [Сс]вои [Оо]ценки',message.text):
        bot.send_message(message.chat.id, 'Напиши номер дз в формате : 1 дз, и я пришлю тебе оценки')
    elif re.match(get_reshenie_regular,message.text):
        bot.send_photo(message.chat.id, photo=y.get_download_link(
            path='/reshenie/' + str(re.search(get_reshenie_regular, message.text).group(1)) + '.jpg'),
                       caption='держи решение к заданию №' + str(
                           re.search(get_reshenie_regular, message.text).group(1)), reply_markup=kb.keyboard_after_reshenie)
    elif re.match(r'[тТ]еперь [Рр]азобрался!',message.text):
        bot.send_message(message.chat.id, 'Так держать !')
    # ask a quection

    elif re.match(r'[зЗ]адать [вВ]опрос [Пп]о [пП]редмету',message.text):
        bot.send_message(message.chat.id,'напиши ему!', reply_markup=kb.keyboard_subject_help)



    elif re.match(r'[Тт]ехническая [Пп]оддержка',message.text):
        bot.send_message(message.chat.id,'По всем тезническам вопросам пиши сюда!', reply_markup=kb.keyboard_tech_help)
    elif message.text == '/help':
        bot.send_message(message.chat.id, 'По всем техническам вопросам пиши сюда!', reply_markup=kb.keyboard_tech_help)
    else:
        bot.send_message(message.chat.id, 'я немного не понял тебя, проверь все ли ты правильно написал!')
        sleep(2)
        bot.send_message(message.chat.id, 'если же ты все правильно написал, но все равно я не отвечаю корректно, напиши в поддержку',reply_markup=kb.keyboard_tech_help)








bot.polling()
