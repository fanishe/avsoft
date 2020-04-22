from parse_link import Parse_Link
from trees import My_Tree
from threads import My_Thread
from logs import Logger
import time
import sys


var = sys.argv[1:]

def main():
    # объект для записи логов и вывода в консоль
    log = Logger()
    log.info(f'START NEW SESSION')
    
    # принимает ссылку через терминал
    # если ничего нет берет основной урл
    if not var:
        link = "https://avsw.ru"
    else:
        link = var[0]

    # Создаем Объект, который парсит главную страницу
    p_link = Parse_Link(link)
    # Список с потоками
    thread_list = []
    start = time.time()

    # Парсим ссылки с главной страницы
    p_link.make_links()
    
    # Создаем потоки по количеству ссылок сохраненных в [list_links]
    for pl in p_link.list_links:
        # передаем ему ссылку из списка главный список для дозаписи новых ссылок и главную ссылку
        t = My_Thread(pl, p_link.list_links, link)
        # сохраняем поток в список и запускаем
        thread_list.append(t)
        t.start()

        log.info(f'{t.getName()} STARTED ')
    # заканчиваем все потоки
    for t in thread_list:
        t.join()
        log.info(f'{t.getName()} KILLED')

    end = time.time()
    # записываю общее время работы парсеров
    log.info(f'Parse time {end - start} sec')

    # сортировка в алфавитном порядке
    p_link.list_links.sort()
    # запись в отделный файл всех ссылок
    p_link.write_to_file()
    
    # создание объекта который будет генерировать карту сайта
    tree = My_Tree()
    # чтение из файла и создание генератора
    generator = tree.read_file(p_link.filename)

    # генерация дерева
    tree.generate_tree(generator)
    # запись дерева в лог и вывод в консоль
    log.info(tree)
    # так же есть возможность вывод на экран с помощью GUI
    tree.show_me()



if __name__ == "__main__":
    main()
    