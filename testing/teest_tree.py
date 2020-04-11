from ete3 import Tree


links_list = [
    '/about',
    '/about/contacts',
    '/about/events',
    '/about/events/event/ImportSub2019',
    '/about/events/event/InfoSecurity2016',
    '/about/events/event/InfoSecurity2017',
    '/about/events/event/InfoSecurity2018',
    '/about/events/event/TBForum2020',
    '/about/sertifikaty',
    '/about/vakansii',
    '/component/content/article/2-uncategorised/4-athena',
    '/components/com_eventgallery/helpers/image.php',
    '/images/agreement/agreement.pdf',
    '/images/athena/scr1.png',
    '/images/athena/scr2.png',
    ''
]

def add_ancestor(tree, l_list):
    for z in l_list[1:]:
        # дальнейшая итерация по составным ссылки
        if z not in tree:
            prev_pos = l_list.index(z)-1
            node = tree&l_list[prev_pos]
            node.add_child(name=z)

def make_list(links):
    links_l = []
    for l in links:
        l = l.split('/')
        links_l.append( l[1:])
        # print(l[1:])
    return links_l

def lets_start(temp_list):
    tree = Tree(format=1)

    for l_links in temp_list:
        if l_links:
            
            if l_links[0] not in tree:
                tree.add_child(name = l_links[0])

                if len(l_links) > 1:
                    # поиск Node в дереве с именем l_links[0]
                    node = tree&l_links[0]
                    add_ancestor(tree, l_links)
                    
                            

            elif l_links[0] in tree and len(l_links) > 1:
                node = tree&l_links[0]
                add_ancestor(tree, l_links)
                    
        else:
            continue
    
    return tree

t_list = make_list(links_list)
tree = lets_start(t_list)
print(tree.get_ascii(show_internal=True))

