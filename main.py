from parse_link import Parse_Link
from trees import My_Tree
from threads import My_Thread, Logger
import time
import sys


var = sys.argv[1:]
# TODO:
    # Что делает код
    # линкер делает запросы
    # парсер парсит полученное и сохраняет ссылки
    # как это должно работать
        # линкер отправляет запросы на все ссылки из главного списка
        # линкер ждет пока парсер закончит
        # главный цикл
            # запускает линкер
            # если пришел ответ отдает его парсеру



def main():
    # объект для записи логов и вывода в консоль
    log = Logger()
    log.write_log(f'START NEW SESSION')
    
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

        log.write_log(f'{t.getName()} STARTED ')
    # заканчиваем все потоки
    for t in thread_list:
        t.join()
        log.write_log(f'{t.getName()} KILLED')

    end = time.time()
    # записываю общее время работы парсеров
    log.write_log(f'Parse time {end - start} sec')

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
    log.write_log(tree)
    # так же есть возможность вывод на экран с помощью GUI
    tree.show_me()



if __name__ == "__main__":
    main()
    