from wikipedia import search, page
from string import punctuation, digits, whitespace
import threading
from multiprocessing import Pool
from collections import deque


class Scrape:
    def __init__(self, *args, **kwargs):
        self.start_title = kwargs['start_title']
        self.file_name = kwargs['file_name']
        self._strp = punctuation + digits + whitespace
        self.content_queue = deque()
        # self.file_object = open(self.file_name, 'a+', encoding='utf8')

    def get_first_page(self):
        titles = search(self.start_title)
        wikipage = page(titles[0])
        return wikipage

    def save(self, link):
        link = link.strip(self._strp)
        try:
            print("saving link {}".format(link))
        except:
            pass
        titles = search(link)
        try:
            wikipage = page(titles[0])
        except Exception as exc:
            # logging the exception
            print(exc.split('\n')[0])
        else:
            self.content_queue.append(wikipage.content)
        # with open(self.file_name, 'a+', encoding='utf8') as f:
        #     f.write(wikipage.content)

    def run_threads(self, links):
        for link in links:
            t = threading.Thread(target=self.save, args=(link,))
            # t.daemon = True
            t.start()
            t.join()
        with open(self.file_name, 'a+', encoding='utf8') as f:
            while True:
                try:
                    f.write(self.content_queue.pop=())
                except:
                    break
        # pool = ThreadPool()
        # pool.map(self.save, links)
        # pool.close()
        # pool.join()

    def dispatcher(self):
        links = self.initial_page.links
        print("{} links founded...".format(len(links)))
        n = len(links) // 4
        with Pool(processes=4) as p:
            p.map(self.run_threads, [tuple(links[n * i:n * (i + 1)]) for i in range(4)])

    def run(self):
        self.initial_page = self.get_first_page()
        self.dispatcher()
