import re
import unicodedata
class Tokenizer:
    def __init__(self, corpus):
        self.corpus = corpus
        self.total_units = 0  
    def _remove_punctuation(self, text):
        return re.sub(r'[^\w\s]', '', text)
    def _remove_stop_words(self, tokens, stop_words):
        return [token for token in tokens if token not in stop_words]    
    def tokenize(self, remove_punctuation=True, stop_words=None):
        text_to_tokenize = ' '.join(self.corpus)
        if remove_punctuation:
            text_to_tokenize = self._remove_punctuation(text_to_tokenize)
        tokens = text_to_tokenize.split()
        if stop_words:
            tokens = self._remove_stop_words(tokens, stop_words)
        return tokens

