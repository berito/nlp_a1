import random
import re
class CorpusSplitter:
    def __init__(self, sententences, split_ratio=0.2, random_seed=None):
        self.sententences = sententences
        self.split_ratio = split_ratio
        self.random_seed = random_seed
        if random_seed:
            random.seed(random_seed)
    def split(self):
        random.shuffle(self.sententences)
        num_sentences = len(self.sententences)
        split_index = int(self.split_ratio * num_sentences)
        train_set = self.sententences[:split_index]
        test_set = self.sententences[split_index:]
        train_data = ' '.join(train_set)
        test_data = ' '.join(test_set)
        return train_data, test_data