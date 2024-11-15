import random
class CorpusSplitter:
    def __init__(self, tokens, split_ratio=0.2, random_seed=None):
        self.tokens = tokens
        self.split_ratio = split_ratio
        self.random_seed = random_seed
        if random_seed:
            random.seed(random_seed)

    def split_by_words(self):
        random.shuffle(self.tokens)
        test_size = int(len(self.tokenized_corpus) * self.split_ratio)
        num_tokens = len(self.tokens)
        split_index = int(self.split_ratio * num_tokens)
        train_set = self.tokenized_corpus[:split_index]
        test_set = self.tokenized_corpus[split_index:]
        train_data = ' '.join(train_set)
        test_data = ' '.join(test_set)
        return train_data, test_data

    def split_by_sentences(self, sentence_separator='፡'):
        sentences = ' '.join(self.tokens).split(sentence_separator)
        random.shuffle(sentences)
        num_sentences = len(self.tokens)
        split_index = int(self.split_ratio * num_sentences)
        train_set = self.tokenized_corpus[:split_index]
        test_set = self.tokenized_corpus[split_index:]
        train_data = sentence_separator.join(train_set)
        test_data = sentence_separator.join(test_set)
        return train_data, test_data