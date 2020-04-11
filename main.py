from parse_link import Parse_Link
from trees import My_Tree
from threads import My_Thread, Logger
import time
    
        
def main():
    log = Logger()
    log.write_log(f'START NEW SESSION')
    
    link = "https://avsw.ru"
    p_link = Parse_Link(link)
    thread_list = []
    start = time.time()

    p_link.make_links()
    
    for pl in p_link.list_links:
        
        t = My_Thread(pl, p_link.list_links, link)
        thread_list.append(t)
        t.start()

        log.write_log(f'{t.getName()} STARTED ')
        
    for t in thread_list:
        t.join()
        log.write_log(f'{t.getName()} KILLED')

    end = time.time()
    log.write_log(f'Parse time {end - start} sec')

    
    p_link.list_links.sort()
    p_link.write_to_file()
    
    tree = My_Tree()
    tree.read_file(p_link.filename)

    tree.generate_tree()

    log.write_log(tree.tree.get_ascii(show_internal=True))
    
    tree.show_me()



if __name__ == "__main__":
    main()
    