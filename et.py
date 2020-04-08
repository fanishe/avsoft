from ete3 import Tree

# Example
# unrooted_tree = Tree( "(A,B,(C,D));" )
# rooted_tree = Tree( "((A,B),(C,D));" )
# t = Tree("((((a,a,a)a,a)aa, (b,b)b)ab, (c, (d,d)d)cd);", format=1)

# unrooted_tree = Tree( "(A,B,(C,D));" )
# rooted_tree = Tree( "((A,B),(C,D));" )
# tt = Tree("((((1,2,3)AA,a)aa, (b,b)b)ab, (c, (d,d)d)cd);", format=1)

# domain = Tree("(D(A,(1,2),B));")
# print(rooted_tree)
# print(t)
# print(t.get_ascii(show_internal=True))

# t = Tree() # Creates an empty tree
# A = t.add_child(name="A") # Adds a new child to the current tree root
#                            # and returns it
# B = t.add_child(name="B") # Adds a second child to the current tree
#                            # root and returns it
# C = A.add_child(name="C") # Adds a new child to one of the branches
# D = C.add_sister(name="D") # Adds a second child to same branch as
#                              # before, but using a sister as the starting
#                              # point
# R = A.add_child(name="R")
# print(t.get_ascii(show_internal=True))


# nw = """(((A:0.01, B:0.01), C:0.0001):1.0,
#     (((((D:0.00001,I:0):0,F:0):0,G:0):0,H:0):0,
#                 E:0.000001):0.0000001):2.0;"""
# t = Tree(nw)

# nw = """
# ((analysis-of-malware)services, (contacts)about);
# """
# nw = """
# ((analysis-of-malware, documents-development)services, (contacts, events)about);
# """
# t = Tree(nw, format=1)
# print(t.get_ascii(show_internal=True))

temp_list = []
with open('domains.txt') as f:
    links = f.read().splitlines()

    for l in links:
        l = l.split('/')
        temp_list.append( l[1:])
# TODO:
    # придумать как называть родителя и как присваивать ему детей
    # вариант 1
        # список со словарями
            # [ {'about': ['contacts', 'events']}, {'products': ['athena', 'octopus']} ]
            # так будет проще дать ему родителя и детей

    # вариант 2
        # сплошной список со списками
            # [ ['about', 'contacts', 'events'], ['products', 'athena', 'octopus'] ]
    
    # вариант 3
        # сделать все автоматом в () и сделать дерево, посмотрим что из этого получится
        


for t in temp_list:
    # if t[0] == 
    pass