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

    def write_to_log(self, level, log):

        with open(self.filename, 'a+') as f:
            log = f'{datetime.now()} {level} - {log}\n'
            f.write(log)
            
            if self.onprint:
                print(log)

    def warning(self, log):
        warn = '[WARNING]'
        self.write_to_log(warn, log)
    
    def debug(self, log):
        warn = '[DEBUG]'
        self.write_to_log(warn, log)

    def info(self, log):
        warn = '[INFO]'
        self.write_to_log(warn, log)

    def error(self, log):
        warn = '[ERROR]'
        self.write_to_log(warn, log)

    def critical(self, log):
        warn = '[CRITICAL]'
        self.write_to_log(warn, log)
