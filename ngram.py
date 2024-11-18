from collections import defaultdict
from typing import List, Tuple, Dict
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class NGram:
    def __init__(self, tokens: List[str]):
        """
        Initialize the NGram class with a list of tokens.
        :param tokens: List of words (tokens) from input text.
        """
        self._tokens = tokens
        self._ngram_dict = None
        self._ngram_probabilities = None

    def generate(self, n: int) -> None:
        ngram_dict = defaultdict(int)
        for i in range(len(self._tokens) - n + 1):
            ngram = tuple(self._tokens[i:i + n])
            ngram_dict[ngram] += 1
        self._ngram_dict = dict(ngram_dict)
        self._ngram_probabilities = None  # Invalidate probabilities if n-grams change

    def _calculate_probabilities(self) -> None:
        if self._ngram_dict is None:
            raise ValueError("N-grams have not been generated. Call `generate()` first.")
        total_count = sum(self._ngram_dict.values())
        self._ngram_probabilities = {
            ngram: count / total_count for ngram, count in self._ngram_dict.items()
        }
    
    def probabilities(self) -> Dict[Tuple[str, ...], float]:
        """
        Get probabilities for the generated n-grams.
        :return: Dictionary of n-grams and their probabilities.
        """
        if self._ngram_probabilities is None:
            self._calculate_probabilities()
        return self._ngram_probabilities
    
    def conditional_probabilities(self) -> Dict[Tuple[str, ...], float]:
        if self._ngram_dict is None:
            raise ValueError("N-grams have not been generated. Call `generate()` first.")   
        conditional_probs = defaultdict(float)
        prefix_dict = defaultdict(int)
        for ngram, count in self._ngram_dict.items():
            if len(ngram) > 1:
                prefix = ngram[:-1]
                prefix_dict[prefix] += 1
        for ngram, count in self._ngram_dict.items():
            if len(ngram) > 1:
                prefix = ngram[:-1]
                prefix_count = prefix_dict.get(prefix, 0)
                print(f"prefix count {prefix}:{prefix_count}")
                if prefix_count > 0:
                    conditional_probs[ngram] = count / prefix_count
                else:
                    conditional_probs[ngram] = 0.0  # In case prefix is not found

        return conditional_probs
    
    def top_frequencies(self, top_k: int) -> List[Tuple[Tuple[str, ...], int]]:
        if self._ngram_dict is None:
            raise ValueError("N-grams have not been generated. Call `generate()` first.")
        return sorted(self._ngram_dict.items(), key=lambda item: item[1], reverse=True)[:top_k]
    
    def display(self) -> None:
        if self._ngram_dict is None:
            raise ValueError("N-grams have not been generated. Call `generate()` first.")
        for ngram, freq in self._ngram_dict.items():
            print(f"{' '.join(ngram)}: {freq}")
    
    def display_conditional_probabilities(self) -> None:
        conditional_probs = self.conditional_probabilities()
        for ngram, prob in conditional_probs.items():
            prefix = ' '.join(ngram[:-1])
            word = ngram[-1]
            print(f"P({word} | {prefix}) = {prob:.4f}")
    
    def create_wordcloud(self, title):
        if self._ngram_dict is None:
            raise ValueError("N-grams have not been generated. Call `generate()` first.")
        font_path="amharic_font.ttf"
        ngram_freq = {" ".join(k): v for k, v in self._ngram_dict.items()}
        wordcloud = WordCloud(width=800, height=400, background_color="white",font_path=font_path).generate_from_frequencies(ngram_freq)
        # Plot the word cloud
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title(title, fontsize=20)
        plt.show()