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

y = yadisk.YaDisk(token="AgAAAAAFCrD9AAaFsnHBigAYx0Vyg5V-BjRKiZs")

excel_path_marks = './marks.xlsx'
excel_path_names = './names_bot.xlsx'
excel_path_check_homework = 'https://yadi.sk/d/bG8jJj4-8aiR0Q'
df_names = pd.DataFrame({
    'сhat_id': ['2020'],
    'name': ['test'],
    'username': ['@kuzmin_andre']
                         })

# сделать давай решение , нет
# сделать блок после подсказок с решением 
try:
    pd.read_excel(excel_path_names)
except FileNotFoundError:
    writer = pd.ExcelWriter(excel_path_names, engine='xlsxwriter')
    df_names.to_excel(writer, 'names')
    writer.save()
df_names_2 = pd.read_excel(excel_path_names,index_col=0)
bot = telebot.TeleBot('1287969362:AAFGI-capLkHpSN3QbrwSgZ-NcxzEzFlALc')
name_regular = r'\s*[мМ]еня\s+[зЗ]овут\s+.*\s*'
number_check_regular = r'\s*((\d+)\.(\d+))\)\s*(.+)\s*'

get_podskaska_regular = r'\s*((\d+)\.(\d+))\)\s*(.+)\s*'
get_reshenie_regular = r'\s*((\d+)\.(\d+))\s*[Рр]ешение\s*'
marks_check_regular = r'\s*(\d+)\s*(.+)\s*'
get_podskaska_regular_2 = r'\s*((\d+)\.(\d+))\.(.+)'
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
    sleep(1)
    bot.send_message(message.chat.id,'Если пока все понятно , нажми на клавиатуре хорошо, если же уже появились вопросы, напиши или нажми на  /help', reply_markup=kb.keyboard_start)
@bot.message_handler(commands=['help'])
def help_tech(message):
    bot.send_message(message.chat.id,'По всем техническим вопросам пиши сюда',reply_markup = kb.keyboard_tech_help)
@bot.message_handler(content_types=['text'])

def get_contact_from(message):

    global df_names_2
    if str(message.from_user.username) == 'NikVarf':
        bot.send_message(message.chat.id,'Добрый день, мой Господин-преподаватель! Для вас есть специальные функции, предложенные в клавиатуре. Удачной работы, Господин!')
    if message.text == 'Хорошо':
        bot.send_message(message.chat.id, 'Давай тогда познакомимся?',reply_markup=kb.keyboard_get_name)
    elif message.text == 'давай, как ни как учиться вместе':
        bot.send_message(message.chat.id, 'Напиши свое имя в формате : меня зовут ...')

    elif re.match(name_regular, message.text):
        # ? не будет ли лажать
        df_check = df_names_2['сhat_id'] == message.chat.id

        if (df_check.any()) != True:
            bot.send_message(message.chat.id, 'Рад познакомиться, ' + str(re.findall(name_regular, message.text)[0][11:]))

            bot.send_message(message.chat.id, 'Если ты случайно ошибся в имени, или ты вдруг'
                                              ' сходишь  в паспорный стол и поменяешь его, '
                                              'напиши "поменять имя"', reply_markup=kb.keyboard_change_name)
            # df_student = pd.DataFrame({'сhat_id': [message.chat.id],
            #                                      'name': [str(re.findall(name_regular, message.text)[0][11:])],
            #                             'username': [str(message.from_user.username)]})
            # try:
            df_marks = pd.read_excel(y.get_download_link(path='/bot-tables/marks.xlsx'),
                                              sheet_name='marks', converters={'Number': str})
            df_marks.index = df_marks['Number/chat_id']
            # df_marks[str(message.chat.id)] = ''
            df_marks.loc['username',message.chat.id] = message.from_user.username
            # df_marks = df_marks.drop('Number/chat_id',1)
            writer = pd.ExcelWriter(excel_path_marks, engine='xlsxwriter')
            df_marks.drop('Number/chat_id',1).to_excel(writer, 'marks')
            writer.save()
            y.upload(path_or_file='./marks.xlsx', dst_path='/bot-tables/marks.xlsx', overwrite=True)

            df_names_2 = df_names_2.append(pd.DataFrame({'сhat_id': [message.chat.id],
                                                 'name': [str(re.findall(name_regular, message.text)[0][11:])],
                                        'username': [str(message.from_user.username)]}),ignore_index=True)
            writer = pd.ExcelWriter(excel_path_names, engine='xlsxwriter')
            df_names_2.to_excel(writer, 'names')
            writer.save()
            y.upload(path_or_file='./names_bot.xlsx',dst_path='/bot-tables/names_bot.xlsx',overwrite =True)
        # except





        else:
            index = df_names_2.loc[df_names_2['сhat_id'] == message.chat.id].index[0]
            df_names_2.loc[index,'name'] = str(re.findall(name_regular, message.text)[0][11:])
            df_names_2.loc[index,'username'] = str(message.from_user.username)

            bot.send_message(message.chat.id,'Хорошо,теперь я буду тебя называть так',reply_markup=kb.keyboard_change_name)
            writer = pd.ExcelWriter(excel_path_names, engine='xlsxwriter')
            df_names_2.to_excel(writer,'names')
            writer.save()
            index = 0
            y.upload(path_or_file='./names_bot.xlsx',dst_path='/bot-tables/names_bot.xlsx',overwrite =True)

    # дописать аналогично обновление столбца
    # нужно сделать перву строчкуу из chat id чтобы при смене имени было удобней и при его отсутсвии все равно
    #




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
    # elif message.text == 'тест':
    #     bot.send_message(message.chat.id, message.chat.id)
    #     bot.register_next_step_handler(message,checking_homework)
    # elif message.text == 'делит':
    #     indexx = df_names_2.loc[df_names_2['сhat_id'] == message.chat.id].index[0]
    #     df_names_2 = df_names_2.drop(index=indexx)
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
        df_marks = pd.read_excel(y.get_download_link(path='/bot-tables/marks.xlsx'),
                                 sheet_name='marks', converters={'Number': str})
        df_marks.index = df_marks['Number/chat_id']
        if re.match(r'[пП]одсказка', str(re.search(number_check_regular, message.text).group(4))) == None:
            df_check_homework = pd.read_excel(y.get_download_link(path='/bot-tables/test_homework.xlsx'),sheet_name='otvet',converters={'Ответ': str,'number': str})
            df_check_homework.index = df_check_homework['number']
            if df_check_homework.loc[str(re.search(number_check_regular, message.text).group(1)), 'Ответ'] == str(re.search(number_check_regular,message.text).group(4)):
                bot.send_message(message.chat.id,'задание верное')
                bot.send_message(message.chat.id,df_names_2.loc[df_names_2.loc[df_names_2['сhat_id'] == message.chat.id].index[0],'name']+',ты молодец!',reply_markup=kb.keyboard_home_menu)

                # df_marks = pd.read_excel(y.get_download_link(path='/bot-tables/marks.xlsx'),
                #                               sheet_name='marks', converters={'Number': str})
                # df_marks.index = df_marks['Number']
                df_marks.loc[str(re.search(number_check_regular, message.text).group(1)),message.chat.id] = 1
                writer = pd.ExcelWriter(excel_path_marks, engine='xlsxwriter')
                df_marks.drop('Number/chat_id',1).to_excel(writer, 'marks')
                writer.save()
                y.upload(path_or_file='./marks.xlsx', dst_path='/bot-tables/marks.xlsx', overwrite=True)
            else:
                bot.send_message(message.chat.id, 'задание неверное(')
                bot.send_message(message.chat.id,df_names_2.loc[df_names_2.loc[df_names_2['сhat_id'] == message.chat.id].index[0],'name']+', подумаешь ещё или хочешь получить подсказку?',reply_markup=kb.keyboard_think_or_help)
                df_marks.loc[str(re.search(number_check_regular, message.text).group(1)),message.chat.id] = 0.5
                writer = pd.ExcelWriter(excel_path_marks, engine='xlsxwriter')
                df_marks.drop('Number/chat_id',1).to_excel(writer, 'marks')
                writer.save()
                y.upload(path_or_file='./marks.xlsx', dst_path='/bot-tables/marks.xlsx', overwrite=True)
        else:
            try:
                    try:
                        bot.send_photo(message.chat.id,photo=y.get_download_link(path='/podskaski/'+str(re.search(get_podskaska_regular,message.text).group(1))+'.jpg'),caption='держи подсказку к заданию №'+str(re.search(get_podskaska_regular,message.text).group(1)),reply_markup=kb.keyboard_after_helping)
                    except yadisk.exceptions.PathNotFoundError:
                        bot.send_photo(message.chat.id,photo=y.get_download_link(path='/podskaski/'+str(re.search(get_podskaska_regular,message.text).group(1))+'.png'),caption='держи подсказку к заданию №'+str(re.search(get_podskaska_regular,message.text).group(1)),reply_markup=kb.keyboard_after_helping)
            except IndexError:
                bot.send_message(message.chat.id,
                                 'Прости, что-то я не понимаю какой номер тебе подсказать.')
                bot.send_message(message.chat.id, 'Что-то странное, напиши лучше в поддержку',reply_markup=kb.keyboard_tech_help)
    elif re.match(r'[Дд]авай [пП]одсказку', message.text):

        # bot.send_message(message.chat.id, 'напиши в формате : "дз.номер из дз) подсказка".\n'
        #                                   ' К примеру : дз номер 2, номер из домашнего задания 4, тогда 2.4) подсказка')
        # почему не меняется df_marks?
        # не успевает обновляться, может использовать внутреннюю df_marks
        # df_marks = pd.read_excel(y.get_download_link(path='/bot-tables/marks.xlsx'),
        #                          sheet_name='marks', converters={'Number': str})
        df_marks = pd.read_excel('./marks.xlsx',sheet_name='marks', converters={'Number': str})
        df_marks.index = df_marks['Number/chat_id']
        try:

            try:
                bot.send_photo(message.chat.id, photo=y.get_download_link(
                    path='/podskaski/' + str(df_marks.loc[df_marks[message.chat.id] == 0.5].index[0]) + '.jpg'),
                               caption='держи подсказку к заданию №' + str(
                                   df_marks.loc[df_marks[message.chat.id] == 0.5].index[0]), reply_markup=kb.keyboard_after_helping)
            except yadisk.exceptions.PathNotFoundError:
                bot.send_photo(message.chat.id, photo=y.get_download_link(
                    path='/podskaski/' + str(df_marks.loc[df_marks[message.chat.id] == 0.5].index[0]) + '.png'),
                               caption='держи подсказку к заданию №' + str(
                                   df_marks.loc[df_marks[message.chat.id] == 0.5].index[0]),
                               reply_markup=kb.keyboard_after_helping)

            df_marks.loc[df_marks.loc[df_marks[message.chat.id] == 0.5].index[0],message.chat.id] = 0
            writer = pd.ExcelWriter(excel_path_marks, engine='xlsxwriter')
            df_marks.drop('Number/chat_id', 1).to_excel(writer, 'marks')
            writer.save()
            y.upload(path_or_file='./marks.xlsx', dst_path='/bot-tables/marks.xlsx', overwrite=True)
        except IndexError:
            bot.send_message(message.chat.id,'Прости, что-то я не понимаю какой номер тебе подсказать. Напиши НОМЕР_ДЗ.НОМЕР_ЗАДАНИЯ) подсказка.')
            bot.send_message(message.chat.id,'К примеру, 1.2) подсказка')

    elif re.match(r'[Пп]опробую [рР]ешить [сС]ам',message.text):
        bot.send_message(message.chat.id,'Молодец! Всегда старайся думать сам.',reply_markup=kb.keyboard_home_menu)

    # подсказку попробовать переделать
    # через 0.5 нахождение в столбце

    elif re.match(r'[Дд]авай [рР]ешение', message.text):

        bot.send_message(message.chat.id, 'напиши в формате : "НОМЕР_ДЗ.НОМЕР решение".\n'
                                          ' К примеру : дз номер 2, номер из домашнего задания 4, тогда 2.4) решение')
    # получение решение
    # может сделать через 
    elif re.match(get_reshenie_regular,message.text):
        try:
            bot.send_photo(message.chat.id, photo=y.get_download_link(
                path='/reshenie/' + str(re.search(get_reshenie_regular, message.text).group(1)) + '.jpg'),
                           caption='держи решение к заданию №' + str(
                               re.search(get_reshenie_regular, message.text).group(1)), reply_markup=kb.keyboard_after_reshenie)
        except yadisk.exceptions.PathNotFoundError:
            bot.send_photo(message.chat.id, photo=y.get_download_link(
                path='/reshenie/' + str(re.search(get_reshenie_regular, message.text).group(1)) + '.png'),
                           caption='держи решение к заданию №' + str(
                               re.search(get_reshenie_regular, message.text).group(1)),
                           reply_markup=kb.keyboard_after_reshenie)

    elif re.match(r'[пП]одумаю [еЕ]щё!',message.text):
        bot.send_message(message.chat.id,'Хорошо, так держать!',reply_markup=kb.keyboard_home_menu)
        df_marks = pd.read_excel(y.get_download_link(path='/bot-tables/marks.xlsx'),
                                 sheet_name='marks', converters={'Number': str})
        df_marks.index = df_marks['Number/chat_id']
        df_marks.loc[df_marks.loc[df_marks[message.chat.id] == 0.5].index[0], message.chat.id] = 0
        # лажа с нумерацией
        writer = pd.ExcelWriter(excel_path_marks, engine='xlsxwriter')
        df_marks.drop('Number/chat_id', 1).to_excel(writer, 'marks')
        writer.save()
        y.upload(path_or_file='./marks.xlsx', dst_path='/bot-tables/marks.xlsx', overwrite=True)
    #     просмотр оценок

    elif re.match(r'[Пп]осмотреть [Сс]вои [Оо]ценки',message.text):
        bot.send_message(message.chat.id, 'Напиши номер дз в формате : 1 дз, и я пришлю тебе оценки. (1 - номер домашнего задания')
    elif re.match(marks_check_regular,message.text):
        df_marks = pd.read_excel(y.get_download_link(path='/bot-tables/marks.xlsx'),
                                 sheet_name='marks', converters={'Number': str})
        df_marks.index = df_marks['Number/chat_id']
        bot.send_message(message.chat.id,str(int(df_marks.loc[str(re.match(marks_check_regular,message.text).group(1))+'.1':str(re.match(marks_check_regular,message.text).group(1))+'.13',message.chat.id].sum()))+' / 13 баллов')


    elif re.match(r'[тТ]еперь [Рр]азобрался!',message.text):
        bot.send_message(message.chat.id, 'Так держать !',reply_markup=kb.keyboard_home_menu)
    # ask a quection

    elif re.match(r'[зЗ]адать [вВ]опрос [Пп]о [пП]редмету',message.text):
        bot.send_message(message.chat.id,'Напиши ему!', reply_markup=kb.keyboard_subject_help)
    elif re.match(r'[Вв]се [рР]авно [нН]е [пП]онял, [оО]стались [вВ]опросы',message.text):
        bot.send_message(message.chat.id,'Напиши ему!', reply_markup=kb.keyboard_subject_help)



    elif re.match(r'[Тт]ехническая [Пп]оддержка',message.text):
        bot.send_message(message.chat.id,'По всем техническам вопросам пиши сюда!', reply_markup=kb.keyboard_tech_help)
    elif message.text == '/help':
        bot.send_message(message.chat.id, 'По всем техническам вопросам пиши сюда!', reply_markup=kb.keyboard_tech_help)
    # statistic for students
    # elif re.match(r'[Сс]татистика по задачам',message.text):













    else:
        bot.send_message(message.chat.id, 'Я немного не понял тебя, проверь все ли ты правильно написал!')
        sleep(2)
        bot.send_message(message.chat.id, 'Если же ты все правильно написал, но все равно я не отвечаю корректно, напиши в поддержку',reply_markup=kb.keyboard_tech_help)

# statistic for students

# добавить try/except в места где используются таблицы чтобы при редактирование не ломался бот yadisk.exceptions.ResourceIsLockedError
# добавить статистику
#  добавить возможно функции закидывания в файлы

# почему то присылал и подсказку и не могу понять что за номер




bot.polling()
