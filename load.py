import gzip
from xml.dom.minidom import Element
from lxml import etree
import time

from document import Abstract

def load_documents():
    file_path = input("Enter the file path for the gzipped dump: ")
    start = time.time()
    #open a filehandle to the gzipped dump
    with gzip.open(file_path) as f:
        doc_id = 0
        # iterparse will yield the entire 'doc' element once it finds the
        # closing '</doc>' tag
        for _, element in etree.iterparse(f, events=('end',), tag='doc'):
            title = element.findtext('./title')
            url = element.findtext('./url')
            abstract = element.findtext('./abstract')

            yield Abstract(ID = doc_id, title=title, url=url, abstract=abstract)

            # the 'element.clear()' call will explicitly free up the memory
            # used to store the element
            doc_id += 1
            element.clear()
        end = time.time()
        print(f'Parsing XML took {end - start} seconds')
