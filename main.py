from parse_link import Parse_Link
from trees import Make_Tree


def main():
    link = "https://avsw.ru"
    p_link = Parse_Link(link)
    p_link.make_links()
    p_link.write_to_file()
    

    tree = Make_Tree()
    tree.read_file(p_link.filename)
    tree.lets_start()
    print(tree.tree.get_ascii(show_internal=True))


if __name__ == "__main__":
    main()
    