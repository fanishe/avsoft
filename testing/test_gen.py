# a = [i ** 2 for i in range(1, 6)]
# # print(a)


# b = (i ** 2 for i in range(1, 6))
# print('generator', b)
# l = list(b)
# print(type(l))

# Test sort links
list_links = []
hostname = 'domain.ru'
links = [
    'https://domain.ru/about/log',
    'https://domains.ru',
    '/pages/page1'
]

for l in links:
    # забирает href
    # l = link.get('href')

    if l:
        # убираю аргументы из ссылок
        if '?' in l:
            l = l[:l.find('?')]

        if hostname in l:
            # отделить домен
            l = l.split(hostname)
            l = l[-1]

        # if all(not link.startswith(prefix) for prefix in social):
        # for s in social:
        #     # удалить ссылки на соцсеточки
        #     if s in l :
        #         l = 'zero'

        if l.startswith('http') and hostname not in l:
            print('Unused link - ', l )
            l = 'zero'
            
        # сохраняю в список
        if l not in list_links and l != 'zero' and len(l) > 1:
            list_links.append(l)

for l in list_links:
    print(l)