import os.path
import requests
import pickle
import threading
import time
import joblib

from load import load_documents
from index import Index

def index_documents(documents, index, thread_id):
    for i, document in enumerate(documents):
        index.index_document(document)
        if i % 5000 == 0:
            print(f'Thread {thread_id} indexed {i} documents with {threading.active_count()} threads and Process ID {os.getpid()}', end='\r')
    return index

if __name__ == '__main__':
    num_threads = 4
    documents = list(load_documents())
    index = Index()
    threads = []
    start_time = time.time()
    for i in range(num_threads):
        t = threading.Thread(target=index_documents, args=(documents[i::num_threads], index, i+1))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    end_time = time.time()
    print(f'Index contains {len(index.documents)} documents')
    print(f'Time taken for indexing: {end_time-start_time:.2f} seconds')
    joblib.dump(index, 'data/index_dump-small.joblib')


    # index.search('London Beer Flood', search_type='AND')
    # index.search('London Beer Flood', search_type='OR')
    # in this search it used boolean query model to understand what results the user expect.
    # index.search('London Beer Flood', search_type='AND', rank=True)
    # index.search('London Beer Flood', search_type='OR', rank=True)
    # same search but this time it uses ranking for showing results.
