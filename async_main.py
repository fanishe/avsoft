import asyncio
import async_parse as ap
from trees import My_Tree
import sys
from logs import Logger

def main(link):
    # Создаю свой логгер
    log = Logger(onprint=True)

    # старт main() из async_parse.py
    asyncio.run(ap.main(link))
    
    # запись ссылок в файл
    filename = 'async_parsed.txt'
    ap.main_list.sort()
    with open(filename, 'w') as f:
        for link in ap.main_list:
            f.write(f"{link}\n")


    tree = My_Tree()
    # чтение из файла и создание генератора
    tree.generate_tree(filename)
    # запись дерева в лог и вывод в консоль
    log.info(tree)
    # так же есть возможность вывод на экран с помощью GUI
    tree.show_me()

if __name__ == "__main__":
    var = sys.argv[1:]

    if not var:
        link = "https://avsw.ru"
    else:
        link = var[0]
        
    main(link)