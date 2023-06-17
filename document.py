from collections import Counter
from dataclasses import dataclass

import analysis

@dataclass
class Abstract:
    """Wikipedia abstract"""
    ID: int
    title: str
    abstract: str
    url: str

    @property
    def fulltext(self):
        return ' '.join([self.title, self.abstract])

    def analyze(self):
        self.term_frequencies = Counter(analysis.analyze(self.fulltext)) 

    def term_frequency(self, term):
        return self.term_frequencies.get(term, 0)