import threading
import time

def sleeper(n, name):
    print(f"Привет я {name}. Собираюсь поспать")
    time.sleep(n)
    print(f'{name} Проснулся')

t = threading.Thread(target = sleeper, name = 'Thread1', args = (5, 'Thread1'))

thread_list = []
start = time.time()

for i  in range(5):
    t = threading.Thread(target = sleeper,
            name = f'thread {i}',
            args = (5, f'thread {i}'))
    thread_list. append(t)
    t.start()
    print(f'{t.name} has started')

for t in thread_list:
    t.join()

end = time.time()
print(f'time taking {end - start}')
print('all threads done')

