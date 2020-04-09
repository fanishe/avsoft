from ete3 import Tree

class Make_Tree(object):
    def __init__(self):
        self.tree = Tree(format = 1)
        self.temp_list = []
    
    def read_file(self, filename):
        with open(filename) as f:
            links = f.read().splitlines()

            for l in links:
                l = l.split('/')
                self.temp_list.append( l[1:])

    def lets_start(self):
        for t in self.temp_list:
            if t[0] not in self.tree:
                self.tree.add_child(name = t[0])

                if len(t) > 1:
                    l = self.tree&t[0]
                    # l = tree.search_nodes(name=t[0])[0]
                    for z in t[1:]:
                        l.add_child(name = f'-- {z}')


            elif t[0] in self.tree and len(t) > 1:
                # l = tree.search_nodes(name=t[0])[0]
                l = self.tree&t[0]
                if l:
                    for z in t[1:]:
                        l.add_child(name = f'-- {z}')
