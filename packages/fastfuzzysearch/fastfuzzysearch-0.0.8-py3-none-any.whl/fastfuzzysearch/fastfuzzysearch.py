
import re
import pyssdeep
from fastsearch import FastSearch

COLON_PATTERN = re.compile(':')

class FastFuzzySearch:
    def __init__(self, ngram_length, train_step_size=1000, similarity_threshold=70):
        self.ngram_length = ngram_length
        self.train_step_size = train_step_size
        self.fastsearch = FastSearch(COLON_PATTERN, self.ngram_length)
        self.is_trained = False
        self.kb_size = 0
        self.final_automaton_ngrams = {}
        self.similarity_threshold = similarity_threshold

    def add_ssdeep_hash(self, ssdeep_hash: str, descriptor: dict, ngram_whitelist=None):
        ngram_set = self.fastsearch.add_sentence(ssdeep_hash, selection_start=1, append_automaton=False)
        if ngram_whitelist:
            ngram_set = ngram_set - ngram_whitelist
        
        low_entropy_set = set()
        for ngram in ngram_set:
            if self.count_unique_chars(ngram) <= self.ngram_length / 2:
                low_entropy_set.add(ngram)
        if len(low_entropy_set) > 0:
            ngram_set = ngram_set - low_entropy_set

        if self.kb_size > 0 and self.kb_size % self.train_step_size == 0:
            self.fit()
        
        descriptor['ssdeep'] = ssdeep_hash
        matches = None
        if self.is_trained:
            matches = self.lookup(ssdeep_hash, one_match=True)
    
        if not matches:
            add_to_kb = False
            for ngram in ngram_set:
                add_to_kb = True
                if ngram not in self.final_automaton_ngrams:
                    self.final_automaton_ngrams[ngram] = {'appearances': 1, 'descriptor': descriptor}
                else:
                    self.final_automaton_ngrams[ngram]['appearances'] += 1
            if add_to_kb:
                self.kb_size += 1
        else:
            for ngram in ngram_set:
                if ngram in self.final_automaton_ngrams:
                    self.final_automaton_ngrams[ngram]['appearances'] += 1

    
    def fit(self, finalize=False):
        self.fastsearch = FastSearch(COLON_PATTERN, self.ngram_length)
        for word, descriptor in self.final_automaton_ngrams.items():
            if descriptor['appearances'] > 1 or self.kb_size < 10000:
                self.fastsearch.add_sentence(word, descriptor=descriptor['descriptor'])
        self.fastsearch.fit()
        if finalize:
            self.final_automaton_ngrams.clear()
        self.is_trained = True


    def lookup(self, ssdeep_hash, one_match=False):
        results = []
        matches = self.fastsearch.lookup(ssdeep_hash, one_match=one_match)
        compared_hashes = set()
        for match in matches:
            matched_ssdeep = match['ssdeep']
            if matched_ssdeep not in compared_hashes:
                score = pyssdeep.compare(ssdeep_hash, matched_ssdeep)
                if score > self.similarity_threshold:
                    match['score'] = score
                    results.append(match)
                    compared_hashes.add(matched_ssdeep)
        return results

    def count_unique_chars(self, s):
        char_set = set()
        for ch in s:
            char_set.add(ch)
        return len(char_set)