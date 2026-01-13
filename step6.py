#1

# import json
#
#
# def menu():
#     print(f'   Выберите действие с файлом:\n'
#           f'1. Прочитать файл\n'
#           f'2. Добавить/измненить пары в файле\n'
#           f'3. Удалить пару\n'
#           f'4. Выйти из приложения\n')
#
#
#
# def read(file: str):
#     with open(file, 'r') as file:
#         loaded_data = json.load(file)
#         print(loaded_data)
#
#
#
# def write_pair(file: str):
#     data = dict([input('Введите пару Ключ Значение через пробел').split()])
#     with open(file, 'w') as edit_file:
#         json.dump(data, edit_file)
#
#
# def remove_pair(filename: str):
#     data = input('Введите пару Ключ Значение через пробел').split()
#     key_to_remove = data[0]
#
#     with open(filename, 'r') as file:
#         loaded_data = json.load(file)
#     if data[0] in loaded_data:
#         del loaded_data[key_to_remove]
#
#     with open(filename, 'w') as file:
#         json.dump(loaded_data, file)
#
#
# def input_data() -> str:
#     file = input('Введите имя файла без расширения')
#     return file
#
#
# while True:
#     menu()
#     action = input('Выберите пункт')
#     if action == '4':
#         break
#     file_name = input_data() + '.json'
#     if action == '1':
#         read(file_name)
#     elif action == '2':
#         write_pair(file_name)
#     elif action == '3':
#         remove_pair(file_name)


#2

# import datetime
#
#
# def logger(*, message: str, level = 'INFO') -> None:
#     current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     log_text = f'{current_time} - {level} - {message}'
#     print(log_text)
#
#     with open('log.txt', 'a', encoding='utf-8') as file:
#         file.write(log_text + '\n')
#
#
# logger(message='Двигатель завёлся')
# logger(message='Программа легла!', level='ERROR')
