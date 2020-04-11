from ete3 import Tree, TreeStyle, TextFace

class My_Tree(object):
    def __init__(self):
        self.tree = Tree(format = 1)
        self.temp_list = []
    
    def read_file(self, filename):
        with open(filename) as f:
            links = f.read().splitlines()

            for l in links:
                l = l.split('/')
                self.temp_list.append( l[1:])

    def add_ancestor(self, l_list):
        for z in l_list[1:]:
            # дальнейшая итерация по составным ссылки
            if z not in self.tree:
                prev_pos = l_list.index(z)-1
                node = self.tree&l_list[prev_pos]
                # self.add_face(node)
                node.add_child(name=z)

    def generate_tree(self):
        for l_links in self.temp_list:
            if l_links:

                if l_links[0] not in self.tree:
                    self.tree.add_child(name = l_links[0])

                    if len(l_links) > 1:
                        # поиск Node в дереве с именем l_links[0]
                        node = self.tree&l_links[0]
                        # node.add_face(face=f'{node[0]}')
                        # self.add_face(node)
                        self.add_ancestor(l_links)



                elif l_links[0] in self.tree and len(l_links) > 1:
                    node = self.tree&l_links[0]
                    # self.add_face(node)
                    self.add_ancestor(l_links)

            else:
                continue
        # self.tree.show()

    def show_me(self):
        ts = TreeStyle()
        ts.show_leaf_name = True
        ts.show_branch_length = True
        ts.show_branch_support = True
        self.tree.show(tree_style=ts)
    
    def add_face(self, node):
        text = TextFace(f'{node}')
        text.margin_right = 5
        text.margin_bottom = 5
        node.add_face(face = text, column = 1)
        # print(node)
