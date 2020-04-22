import asyncio

async def g():
    await asyncio.sleep(3)
    print('получил ответ')

async def f():
    # начинаем что-то делать
    var_f = 'парсим урл'
    print(var_f)
    # ждем передачи данных
    # ждем выполнения другой функции
    await g()
    # после ее заавершения продоложаем работать
    print('делаю список из ответа')


async def main():
    await asyncio.gather(f(), f(), f())

asyncio.run(main())
"""
import asyncio

async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")

async def main():
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

"""