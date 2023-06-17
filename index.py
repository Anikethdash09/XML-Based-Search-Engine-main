import math
import concurrent.futures
import multiprocessing
from timing import timing
from analysis import analyze

class Index:
    def __init__(self):
        self.index = {}
        self.documents = {}
        self.avg_doc_length = 0.0

    def index_document(self, document):
        if document.ID not in self.documents:
            self.documents[document.ID] = document
            document.analyze()

        doc_length = len(document.fulltext)
        self.avg_doc_length = (self.avg_doc_length * len(self.documents) + doc_length) / (len(self.documents) + 1)

        for token in analyze(document.fulltext):
            if token not in self.index:
                self.index[token] = []
            self.index[token].append(document.ID)
            # indexing and adding IDs to the list

    def document_frequency(self, token):
        return len(self.index.get(token, []))

    def inverse_document_frequency(self, token):
        df = self.document_frequency(token)
        return math.log((len(self.documents) - df + 0.5) / (df + 0.5))

    def _results(self, analyzed_query):
        return [self.index.get(token, []) for token in analyzed_query]

    @timing
    def search(self, query, search_type, rank=True):
        if search_type not in ('AND', 'OR'):
            return []

        analyzed_query = analyze(query)
        results = self._results(analyzed_query)
        if search_type == 'AND':
            # all tokens must be in the document
            documents = [self.documents[doc_id] for doc_id in set.intersection(*map(set, results))]
        if search_type == 'OR':
            # only one token has to be in the document
           documents = [self.documents[doc_id] for doc_id in set.union(*map(set, results))]

        if rank:
            return self.rank(analyzed_query, documents)
        return documents

    def rank(self, analyzed_query, documents):
        results = []
        if not documents:
            return results
        for document in documents:
            score = 0.0
            doc_length = len(document.fulltext)
            for token in analyzed_query:
                tf = document.term_frequency(token)
                idf = self.inverse_document_frequency(token)
                score += (idf * tf * (1.2 + 1) / (tf + 1.2 * (1 - 0.75 + 0.75 * doc_length / self.avg_doc_length)))
            results.append((document, score))
        return sorted(results, key=lambda doc: doc[1], reverse=True)

    def index_documents_parallel(self, documents):
        with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            for _ in executor.map(self.index_document, documents):
                pass





# concurrent.futures module to create a thread pool executor, 
# which can execute multiple threads concurrently.

# index_document method for indexing using the executor.map()
# why executor_map ?
# executor.map() method takes care of creating and scheduling the threads for execution and returns an iterator that can be used to monitor the progress of the threads.
# this method parallelizes the indexing process by using multiple threads to index the documents in the input list.