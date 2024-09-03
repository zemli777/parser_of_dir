import os.path
import pathlib
import hashlib
from datetime import datetime
from db import connect_db, disconnect_db, take_path_db, add_to_db

def print_file_info(file_path):

    # Получаем информацию о файле
    file_size = os.path.getsize(file_path)
    creation_time = os.path.getctime(file_path)
    last_modified = os.path.getmtime(file_path)

    # Форматируем время
    creation_time_formatted = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
    last_modified_formatted = datetime.fromtimestamp(last_modified).strftime('%Y-%m-%d %H:%M:%S')
    today_time_formatted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Выводим информацию о файле
    # print(f"Информация о файле {file_path}:")
    # print(f"Размер файла: {file_size} байт")
    # print(f"Время создания: {creation_time_formatted}")
    # print(f"Время последнего изменения: {last_modified_formatted}")

    data = [creation_time_formatted, last_modified_formatted, today_time_formatted]
    return data


def add_info(path):

    # Проверяем, существует ли директория
    if not os.path.isdir(path):
        print(f"Каталог {path} не найден.")
        return

    """
    Рекурсивно печатает содержимое каталога.
    :param path: Путь к каталогу.
    """
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            add_info(full_path)
        else:
            #path, size, attr, date_c, date_u, date_l, id_task, flag_t, flag_e
            data = [full_path, os.path.getsize(full_path), type_parser(full_path)] + print_file_info(full_path) + [0, 1, 0]
            add_to_db(data)



def print_directory_contents(path):

    # Проверяем, существует ли директория
    if not os.path.isdir(path):
        print(f"Каталог {path} не найден.")
        return

    """
    Рекурсивно печатает содержимое каталога.
    :param path: Путь к каталогу.
    """
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            print_directory_contents(full_path)
        else:
            # path, size, attr, date_c, date_u, date_l, id_task, flag_t, flag_e
            # data= [full_path, type_parser(full_path)]
            # data.append(print_file_info)
            # print(full_path)
            type_parser(full_path)
            print_file_info(full_path)
            ks_md5(full_path)


def ks_md5(file_path):

    """
    Вычисляет контрольную сумму MD5 файла.
    :param file_path: Путь к файлу.
    :return: Контрольная сумма MD5 файла.
    """
    hash_md5 = hashlib.md5()

    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)

    print(f"Контрольная сумма: {hash_md5.hexdigest()}")
    return hash_md5.hexdigest()


def type_parser(file_path):

    # Определяем тип файла
    file_extension = pathlib.Path(file_path).suffix
    # print(f"Расширение файла: {file_extension}")
    return(file_extension)
    # Если архив



# Пример использования функции
if __name__ == "__main__":
    
    connect_db()
    directory_path = take_path_db(2)
    for path in directory_path:
        #print(path)
        add_info(path)
        #print_directory_contents(path)
    disconnect_db()
    # file_path = input("Введите путь к файлу: ")
    # type_parser(file_path)
    # print_file_info(file_path)
