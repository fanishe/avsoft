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
    



if __name__ == "__main__":
    main()
    