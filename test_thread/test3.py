import threading
import time

class My_Thread(threading.Thread):
    def __init__(self, number, func, args):
        threading.Thread.__init__(self)
        self.number = number
        self.func = func
        self.args = args

    def run(self):
        print(f'{self.getName()} has started ')
        self.func(*self.args)
        print(f'{self.getName()} has finished!')

# def sleeper(n, name):
#     print(f"Привет я {name}. Собираюсь поспать")
#     time.sleep(n)
#     print(f'{name} Проснулся')

def double(number, cycles):
    for i in range(cycles):
        number += number
    print(number)
        


# for i in range(4):
#     t = My_Thread(target = sleeper,
#                 name = (f'thread {i + 1}'),
#                 args = (3, f'thread {i + 1}'))
#     t.start()

thread_list = []

for i in range(5):
    t = My_Thread(number = i + 1, func = double, args=[i, 3])
    thread_list.append(t)
    t.start()

for t in thread_list:
    t.join()