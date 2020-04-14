from ete3 import Tree, TreeStyle, TextFace

class My_Tree(object):
    """
    Это самый интересный объект
        генериррует дерево в консоль или в файл или в GUI
    - Принимает файл сгенерированный Parse_Link()
    - Читает и парсит строки делая из них генератор
    - Генерирует дерево
        * Если ссылки
                /about
                /about/events
                /about/events/event/event1
            = добавляем первый элемент в дерево
            = следующие ссылки прикрепляем как дети предыдущей
        * Если ссылки
                /components/content/article/article-title/Παλλὰς Ἀθηνᾶ
            = из первого элемента делаем ветку дерева
            = каждый элемент ссылки делаем веткой предыдущего
              предварително проверив не является ли элемент веткой
        * Если список пустой пропускаем
    - Открывает GUI и показывает дерево
        но есть ньюанс
            оно не подписывает ветки как в консоли,
                или я не нашел как
            поэтому оно мне не очень нравится
    """
    def __init__(self):
        self.tree = Tree(format = 1)

    def __str__(self):
        return self.tree.get_ascii(show_internal=True)

    def read_file(self, filename):
        with open(filename) as f:
            links = f.read().splitlines()

            for l in links:
                l = l.split('/')
                yield l

    def generate_tree(self, generated_list):
        # генерация дерева
        for l_links in generated_list:
            if l_links:

                if l_links[0] not in self.tree:
                    self.tree.add_child(name = l_links[0])

                    if len(l_links) > 1:
                        # поиск Node в дереве с именем l_links[0]
                        node = self.tree&l_links[0]
                        # self.add_face(node)
                        self.add_ancestor(l_links)

                elif l_links[0] in self.tree and len(l_links) > 1:
                    node = self.tree&l_links[0]
                    # self.add_face(node)
                    self.add_ancestor(l_links)

            else:
                continue
    
    def add_ancestor(self, l_list):
        # Проверяет каждый элемент ссылки,
        # если элемент не является веткой
        # добавляет к предыдущему 
        for z in l_list[1:]:
            if z not in self.tree:
                prev_pos = l_list.index(z)-1

                node = self.tree&l_list[prev_pos]
                # self.add_face(node)
                node.add_child(name=z)

    def show_me(self):
        # GUI
        ts = TreeStyle()
        ts.show_leaf_name = True
        ts.show_branch_length = True
        ts.show_branch_support = True
        self.tree.show(tree_style=ts)
    
    def add_face(self, node):
        # попытка сделать подписи к веткам для GUI
        text = TextFace(f'{node}')
        text.margin_right = 5
        text.margin_bottom = 5
        node.add_face(face = text, column = 1)
