from datetime import datetime

class Logger(object):
    """
    простой объект для ведения логов
    если onprint TRUE:
        в консоль ничего не выводит
    """
    def __init__(self, onprint = True):
        self.filename = 'parser.log'
        self.onprint = onprint

    def write_log(self, log):

        with open(self.filename, 'a+') as f:
            f.write(f'{datetime.now()} - {log}\n')
            
            if self.onprint:
                print(f'{log}\n')