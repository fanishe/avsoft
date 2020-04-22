# Составлеие карты сайта Python

<details>
  <summary></summary>
<img src="testing/mem.webp" alt="mem" style="zoom:25%;" />
</details>

## UPD:
1. Вместо собственного класса Loger для логирования можно было бы
использовать стандартную библеотеку logging

    - _Покрутил, поизучал этот вопрос и пришел к тому, что она для меня неудобная, мне проще написать свой класс со схожими параметрами и его будет легче импортировать, одной строчкой, или я может что-то недоглядел_

2. Потоки можно было бы заменить asyncio, что было бы быстрее
    - _Заменил, пытался заставить эту громадину работать быстрее, но прироста скорости так и не удалось добиться. Держится в районе 12 сек. При сравнении даже потоки начали быстрее летать, всего 3 сек на всесь парсинг. Не могу понять в чем получился затык_

3. Нет распределния ссылок между потоками, потоки закончившие парсинг ссылки простаивают

    - _Не успел обработать этот вопрос, но при парсинге скорость радовала и 3 сек на всю работу даже понравился результат, хотя я ничего не сделал. Пытался функцию `run()`  обернуть в декоратор `@asyncio.coroutine` но это сломало работу потоков, и результат был не тот_

    - _Так же решил вопрос с генератором и применил его в `trees.py` в `read_file()`_

Работа над этим проектом была очень интересной. Открыл для себя много нового. Жалко что не открыл matplotlib, но и до него когда-нибудь доберусь.
Много времени ушло на подбор решения для вывода карты сайта. Мне показалось что библиотека ete3 самый оптимальный вариант особенно если мало опыта
В основном парсинг главного сайта занимает в среднем около 10 сек

#### Есть у кода баг или фича:
Если попадаются ссылки на внешние сайты, или форумы, он начинает парсить и их, и этот процесс затягивается до 5ти минут (тест проводил на сайте python-scripts.com) _Честно скажу, было страшно, было создано около тысячи потоков. Думал, что комп задымится_



### Библиотеки
- [beautifulsoup 4](https://www.crummy.com/software/BeautifulSoup/)
- [ete3](http://etetoolkit.org)
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro)
- [aiohttp](https://aiohttp.readthedocs.io/en/stable/)

Запускаемый код в `main.py` с потоками, или `async_main.py` - асинхронное программирование

## ТЗ

### Написать скрипт на Python, который делает карту любого сайта.

_Требования:_

- [x] Предпочтительно объектно-ориентированный стиль программирования;
- [x] Многопоточная обработка с Python средствами (Multiprocessing, Threading, etc..) или потоки из под языка Си (захват/освобождение GIL);
    - _Использовал Threadimg_
- [x] Итераторы/Генераторы для обхода структуры (в глубину/ширину);
    - _В `trees.py` применил генератор, чтобы обойтись без промежуточного списка_
- [x] Залить на Github/Bitbucket;
- [x] Опционально: сейв карты в базу или рисовать с помощью matplotlib.
    - _Нашел аналог ETE3_