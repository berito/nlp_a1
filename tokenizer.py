import re

class Tokenizer:
    def __init__(self, num_words, data_loader):
        self.num_words = num_words
        self.data_loader = data_loader
        self.corpus = None
        self.total_words = 0

    def _get_text_by_words(self):
        full_text = self.data_loader()
        words = full_text.split()
        self.corpus = ' '.join(words[:self.num_words])
        self.total_words = len(words)

    def _remove_punctuation(self, text):
        return re.sub(r'[^\w\s]', '', text)

    def _remove_stop_words(self, tokens, stop_words):
        return [token for token in tokens if token not in stop_words]

    def tokenize(self, remove_punctuation=True, stop_words=None):
        if self.corpus is None:
            self._get_text_by_words()  # Load the text if not already loaded
        text_to_tokenize = self.corpus  # Work with a copy of the corpus
        if remove_punctuation:
            text_to_tokenize = self._remove_punctuation(text_to_tokenize)
        tokens = text_to_tokenize.split()  # Tokenize into words

        if stop_words:
            tokens = self._remove_stop_words(tokens, stop_words)

        return tokens

