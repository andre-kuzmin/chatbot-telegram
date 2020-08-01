# import yadisk
# import pandas as pd
# from io import BytesIO
# import base64
# bio = BytesIO()
# y = yadisk.YaDisk(token="AgAAAAAFCrD9AAaFsnHBigAYx0Vyg5V-BjRKiZs")
# print(y.check_token('AgAAAAAFCrD9AAaFsnHBigAYx0Vyg5V-BjRKiZs'))
# df = pd.read_excel(y.get_download_link(path='/bot-tables/test_homework.xlsx'))
# print(df)
# df.loc[3, 'Вариант4 '] = 4.4
# df.loc[3, 'Ответ'] = 4.4
# df.loc[0, 'Ответ'] = 3

# print(df)

# writer = pd.ExcelWriter(bio, engine='xlsxwriter')
# df.to_excel(writer)
# output = BytesIO()
#
# # Use the BytesIO object as the filehandle.
# writer = pd.ExcelWriter(output, engine='xlsxwriter')
#
# # Write the data frame to the BytesIO object.
# df.to_excel(writer, sheet_name='Sheet1')
#
# writer.save()
# output.seek(0)
# encoded = base64.b64encode(output.read())
# print(type(encoded))
# writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
# df.to_excel(writer)
# writer.save()
# y.upload(path_or_file=, dst_path='/bot-tables')
#
