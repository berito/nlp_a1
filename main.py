from tokenizer import Tokenizer
from corpus_spliter import CorpusSplitter
from utils import hdf5_data_loader,read_stop_words
import argparse
def test_punctuation_and_load_data():
    #  # Tokenize the text with punctuation removal
    # tokens_with_punctuation_removed = tokenizer.tokenize(remove_punctuation=True)
    # print(f"Tokens (without punctuation): {tokens_with_punctuation_removed}")
    # tokens_with_punctuation = tokenizer.tokenize(remove_punctuation=False)
    # print(f"Tokens (with punctuation): {tokens_with_punctuation}")
    # print(f"Total Words in Corpus: {tokenizer.total_words}")
    # Path to the stop words file
    pass
def stop_word_test():
    num_words = args.num_words
    tokenizer = Tokenizer(num_words, hdf5_data_loader)  # Pass the external loader as a dependency
    stop_words_file = 'stopwords_am.txt'
    stop_words = read_stop_words(stop_words_file)
    tokens = tokenizer.tokenize(remove_punctuation=True, stop_words=stop_words)
    print(f"Tokens (with stop word removal): {tokens}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read text from an HDF5 file and display a specific number of characters.")
    parser.add_argument('--num_words', type=int, default=500, help="Number of characters to display from the text.")
    args = parser.parse_args()
    num_words = args.num_words
    tokenizer = Tokenizer(num_words, hdf5_data_loader)  # Pass the external loader as a dependency
    tokens = tokenizer.tokenize(remove_punctuation=True)
    corpus_splitter = CorpusSplitter(tokens, split_ratio=0.8, random_seed=42)

    # Split the corpus into training and testing sets
    train_set, test_set = corpus_splitter.split()

    # Output the results
    print("Training Set:", train_set)
    print("Test Set:", test_set)
