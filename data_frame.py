# import pandas as pd
# df_names = pd.DataFrame({
#     'chat id': ['289598971','289598970','289598970'],
#     'name': ['aaa','fff','ffff']
#                          })
# excel_path = '/Users/andrejkuzmin/Desktop/names_bot.xlsx'
# df = pd.read_excel(excel_path,index_col = 0)
# print(df, ' df')
# chat_id = '289598971'
# name = 'fylht'
# # df_names._set_value(chat_id,'name','andrey')
# # index = df_names.loc[df_names['chat id'] == chat_id].index[0]
# # print(df_names)
# # df_student = pd.DataFrame({'chat id': [chat_id],
# #                            'name': [name]})
# # df_names.append(df_student,ignore_index=True)
# # print(df_student)
# # df_names = df_names.append(df_student,ignore_index=True)
# # print(df_names)
# # df_check = df['chat_id'] == str(chat_id)
# # print(df_check)
# df_check = df['сhat_id'] == int(chat_id)
# print(df_check)
#
#


print(re.search(regular_num, number).group(2), ' номер')
print(re.search(regular_num, number).group(3), ' ответ')
print(re.search(regular_num, number).group(1), ' номер дз')

index = df.loc[df['Номер задания'] == int(re.search(regular_num, number).group(2))].index[0]
print(index)
if df.loc[index, 'Выбор ответа'] == 'Да':
    print('yes ', df.loc[index, 'Выбор ответа'])
    if re.search(regular_num, number).group(3) == df.loc[index, 'Ответ']:
        print('Задание верное, молодец')
    else:
        print('пиздец ты ебанько')


else:
    print('no')