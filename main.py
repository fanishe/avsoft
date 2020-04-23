from parse_link import Parse_Link
from trees import My_Tree
from threads import My_Thread, ThreadPool
from logs import Logger
import time
import sys
import threads as tr


var = sys.argv[1:]

def main():
    # объект для записи логов и вывода в консоль
    log = Logger()
    log.info(f'START NEW SESSION')
    
    # принимает ссылку и пул(кол-во потоков) через терминал
    # если ничего нет берет основной урл и 50 потоков
    if not var:
        LINK = "https://avsw.ru"
        # LINK = "https://python-scripts.com"
        POOL = 50
    else:
        # можно при вызове постваить один знак
        # если есть желание оставть сайт тот же а кол-во потоков изменить
        # Например $ python main.py - 100
        if len(var[0]) == 1:
            LINK = "https://avsw.ru"
        else:
            LINK = var[0]
        POOL = int(var[1])


    # Создаем Объект, который парсит главную страницу
    p_link = Parse_Link(LINK)
    # Список с потоками
    # thread_list = []
    start = time.time()

    # Парсим ссылки с главной страницы
    p_link.make_links()


    def run(link):
        main_url = LINK
        try:
            url = f'{main_url}{ link}'
            log.info(f'RUN URL - {url}')
            
            # Создается обЪект парсер который извлекает ссылки
            parser = Parse_Link(url)
            parser.make_links()
            
            # Основной список ссылок из главной страницы
            links = parser.list_links
            # Добавление найденных ссылок в основной список
            if links:
                for link in links:
                    if link not in p_link.list_links:
                        p_link.list_links.append(link)
                        log.info(f'ADD LINK - {link}')
            
        except Exception as e:
            log.error(e)

    # Создается пулл с количеством потоков
    pool = ThreadPool(POOL)
    # Его запуск
    pool.map(run, p_link.list_links )
    # Завершение
    pool.wait_completion()

    # ==== Старый код по запуску тредов ====
    # Создаем потоки по количеству ссылок сохраненных в [list_links]
    # for pl in p_link.list_links:
        # передаем ему ссылку из списка главный список для дозаписи новых ссылок и главную ссылку
        # t = My_Thread(pl, p_link.list_links, link)
        # сохраняем поток в список и запускаем
        # thread_list.append(t)
        # t.start()
    
        # log.info(f'{t.getName()} STARTED ')
    # заканчиваем все потоки
    # for t in thread_list:
    #     t.join()
    #     log.info(f'{t.getName()} KILLED')
    # ======== Его наверно надо удалить, но рука не поднимается ======

    end = time.time()
    # записываю общее время работы парсеров
    log.info(f'Parse time {end - start} sec')

    # сортировка в алфавитном порядке
    p_link.list_links.sort()
    # запись в отделный файл всех ссылок
    p_link.write_to_file()
    
    # создание объекта который будет генерировать карту сайта
    tree = My_Tree()

    # генерация дерева
    tree.generate_tree(p_link.filename)
    
    # запись дерева в лог и вывод в консоль
    log.info(tree)
    # так же есть возможность вывод на экран с помощью GUI
    tree.show_me()



if __name__ == "__main__":
    main()
    