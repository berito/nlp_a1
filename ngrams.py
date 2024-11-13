import h5py
import argparse
from read_hd5 import read_hd5
from nltk import ngrams
 # Set up argument parsing to accept the number of characters as a command-line argument
parser = argparse.ArgumentParser(description="Read text from an HDF5 file and display a specific number of characters.")
parser.add_argument('--num_chars', type=int, default=500, help="Number of characters to display from the text.")
args = parser.parse_args()
characters,num_chars_in_text=read_hd5(args.num_chars)
# Print the specified number of characters (from the argument)
print(f"\nFirst {args.num_chars} characters of the content:")
# Print the metadata (total number of characters in the text)
print(f"Total number of characters in the text: {num_chars_in_text}")
print(characters)  # Print the specified number of characters


# Tokenize the text into words
tokens = characters.split()

# Function to generate n-grams
def generate_ngrams(tokens, n):
    return list(ngrams(tokens, n))

# Generate and print n-grams for n=1, 2, 3, 4
for n in range(1, 5):
    print(f"{n}-grams:")
    ngram_list = generate_ngrams(tokens, n)
    for ngram in ngram_list:
        print(ngram)
    print()
