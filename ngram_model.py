import math
from collections import defaultdict
import random
class NgramModel:
    def __init__(self, n,alpha):
        self.n = n
        self.ngram_counts = defaultdict(int)  
        self.context_counts = defaultdict(int)  # Counts for (n-1)-gram contexts
        self.vocab = set() # smothing
        self.alpha = alpha # smothing
    def train(self, corpus):
        for sentence in corpus:
            if isinstance(sentence, str):
                sentence = sentence.split()  # Tokenize if it's a string
            elif not isinstance(sentence, list):
                continue  # Skip if not a valid sentence format   
            # tokens = ["<s>"] * (self.n - 1) + sentence + ["</s>"]
            # tokens = ["<s>"] + sentence + ["</s>"]
            # # self.vocab.update(tokens) # smothing
            # for i in range(len(tokens) - self.n + 1):
            #     ngram = tuple(tokens[i:i + self.n])
            #     context = tuple(tokens[i:i + self.n - 1])
            #     self.ngram_counts[ngram] += 1
            #     self.context_counts[context] += 1
        for sentence in corpus:
            # Add start and end tokens
            tokens = ["<s>"] * (self.n - 1) + sentence.split() + ["</s>"]
            for i in range(len(tokens) - self.n + 1):
                # Extract n-gram and (n-1)-gram context
                ngram = tuple(tokens[i:i + self.n])
                context = ngram[:-1]
                
                # Update counts
                self.ngram_counts[ngram] += 1
                self.context_counts[context] += 1
    def ngram_probability(self, ngram):
        """Calculate the probability of an n-gram."""
        context = ngram[:-1]
        return self.ngram_counts[ngram] / self.context_counts[context] if self.context_counts[context] > 0 else 0
        # with smothing
        # context = ngram[:-1]
        # context_count = self.context_counts[context]
        # ngram_count = self.ngram_counts[ngram]
        # V = len(self.vocab)
        # return (ngram_count + self.alpha) / (context_count + self.alpha * V)
    def _get_probability(self, word, context):
        ngram = context + (word,)
        return self.ngram_counts[ngram] / self.context_counts[context] if self.context_counts[context] > 0 else 0
    def perplexity(self, test_corpus):
        """Calculate perplexity on a test corpus."""
        log_prob_sum = 0
        word_count = 0 
        for sentence in test_corpus:
            if isinstance(sentence, str):
                sentence = sentence.split()  # Tokenize if it's a string
            elif not isinstance(sentence, list):
                continue  # Skip if not a valid sentence format
            # Add start and end tokens
            # tokens = ["<s>"] * (self.n - 1) + sentence + ["</s>"]
            tokens = ["<s>"] + sentence + ["</s>"]
            # Iterate over n-grams
            for i in range(len(tokens) - self.n + 1):
                ngram = tuple(tokens[i:i + self.n])
                prob = self.ngram_probability(ngram)
                # If the n-gram probability is greater than zero, take its log probability
                if prob > 0:
                    log_prob_sum += math.log(prob)
                else:
                    # Assign a very small probability to unseen n-grams (Laplace smoothing)
                    log_prob_sum += math.log(1e-6)
                
                # Increase word count excluding padding tokens
                if tokens[i + self.n - 1] != "</s>":
                    word_count += 1

        # Calculate average log probability and then perplexity
        avg_log_prob = log_prob_sum / word_count
        perplexity = math.exp(-avg_log_prob)
        return perplexity
    def generate(self, max_words=20):
        context = ("<s>",) * (self.n - 1)
        sentence = []
        for _ in range(max_words):
            word = self._sample(context)
            if word == "</s>":
                break
            sentence.append(word)
            context = context[1:] + (word,)  # Update context with the new word
        
        return " ".join(sentence)
    def _sample(self, context):
        candidates = [ngram[-1] for ngram in self.ngram_counts if ngram[:-1] == context]
        
        # If no candidates are found, fallback to <s> or any default word
        if not candidates:
            return "</s>"  # End token to stop generation or fallback to another token
        
        probabilities = [self._get_probability(word, context) for word in candidates]
        
        # Normalize probabilities
        total_prob = sum(probabilities)
        
        # If total_prob is zero, use uniform probability distribution
        if total_prob == 0:
            normalized_probs = [1 / len(candidates)] * len(candidates)
        else:
            normalized_probs = [p / total_prob for p in probabilities]
        
        # Sample from candidates based on probabilities
        return random.choices(candidates, weights=normalized_probs, k=1)[0]