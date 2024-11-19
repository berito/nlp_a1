import random
import re
class CorpusSplitter:
    def __init__(self, sentences, stopwords=None,split_ratio=0.2, random_seed=None):
        self.sentences = sentences
        self.split_ratio = split_ratio
        self.random_seed = random_seed
        self.stopwords=stopwords
        if random_seed:
            random.seed(random_seed)
    def remove_stopwords(self, sentence):
        removed=' '.join([word for word in sentence.split() if word not in self.stopwords])
        return removed
    def count_total_words(self, sentences):
     return sum(len(sentence.split()) for sentence in sentences)
    def split(self):
        # # Check if sentences are properly formatted as strings
        # print("Sample sentences before processing:", self.count_total_words(self.sentences))
        if self.stopwords:
            tokenized_sentences = [self.remove_stopwords(sentence) for sentence in self.sentences]
        else:
            tokenized_sentences =self.sentences  # Ensure sentences are tokenized
        # print("Sample sentences after processing:", self.count_total_words(tokenized_sentences))
        random.shuffle(tokenized_sentences)
        num_sentences = len(tokenized_sentences)
        split_index = int(self.split_ratio * num_sentences)
        train_data = tokenized_sentences[:split_index]
        test_data = tokenized_sentences[split_index:]
        # train_data = ' '.join(train_set)
        # test_data = ' '.join(test_set)
        return train_data, test_data