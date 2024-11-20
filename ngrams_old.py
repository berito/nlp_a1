import argparse
import random
from read_hd5 import read_hd5,get_text_by_words
from collections import defaultdict
import matplotlib.pyplot as plt
from wordcloud import WordCloud
 # Set up argument parsing to accept the number of characters as a command-line argument
parser = argparse.ArgumentParser(description="Read text from an HDF5 file and display a specific number of characters.")
# parser.add_argument('--num_chars', type=int, default=500, help="Number of characters to display from the text.")
parser.add_argument('--num_words', type=int, default=500, help="Number of characters to display from the text.")

args = parser.parse_args()
# corpus,num_chars_in_text=read_hd5(args.num_chars)
corpus,num_of_words=get_text_by_words(args.num_words)
# Print the specified number of characters (from the argument)
# print(f"\nFirst {args.num_chars} characters of the content:")
# Print the metadata (total number of characters in the text)
print(f"Total number of words in the text: {num_of_words}")
print(corpus)  # Print the specified number of characters

# Tokenize the text into words
tokens = corpus.split()

def generate_ngrams(tokens, n):
    ngram_dict = defaultdict(int)
    for i in range(len(tokens) - n + 1):
        ngram = tuple(tokens[i:i + n])
        ngram_dict[ngram] += 1
    return dict(ngram_dict)


def print_ngram(ngram_dict,n):
    print(f"{n}-grams:")
    for ngram, count in ngram_dict:
        print(f'{ngram}:{count}')    
    print() 
def print_ngram_probability(ngram_prob,n,format):
    print(f"{n}-grams:")
    for ngram, prob in ngram_prob:
            print(f'{ngram}:{prob:.6f}')

def print_bigram_condtional_probabilities(ngram_prob,n):
    print(f"{n}-grams:")
    for ngram, prob in ngram_prob.items():
        print(f'{ngram}:{prob:.6f}')
# the two functions below have same functionality
# one accets the ngram_dict from outside and the other accepts the token
def calculate_ngram_probabilities(ngram_dict):
    total_count = sum(ngram_dict.values())
    ngram_probabilities = {ngram: count / total_count for ngram, count in ngram_dict.items()}
    return ngram_probabilities
def build_corpus_ngram_probabilities(tokens, n):
    ngrams = generate_ngrams(tokens, n)
    total_ngrams = sum(ngrams.values())  
    # Calculate probabilities
    ngram_probabilities = {ngram: count / total_ngrams for ngram, count in ngrams.items()}
    return ngram_probabilities

def calculate_sentence_probability(sentence_tokens, ngram_probabilities, n):
    sentence_ngrams = generate_ngrams(sentence_tokens, n)
    sentence_prob = 1.0
    for ngram, count in sentence_ngrams.items():
        if ngram in ngram_probabilities:
            sentence_prob *= ngram_probabilities[ngram] ** count  # Multiply with probability for each occurrence of the ngram
        else:
            sentence_prob *= 0  # If n-gram not found in the probabilities, assume probability 0

    return sentence_prob

def find_top_ngrams_by_proability(ngram_probabilities, top_k=10):
    return sorted(ngram_probabilities.items(), key=lambda item: item[1], reverse=True)[:top_k]
def find_top_ngrams_by_frequency(ngram_frequency, top_k=10):
    return sorted(ngram_frequency.items(), key=lambda item: item[1], reverse=True)[:top_k]
# Function to create a word cloud
def create_wordcloud(ngram_dict, title):
    font_path="amharic_font.ttf"
    # Convert n-gram tuples to strings
    ngram_freq = {" ".join(k): v for k, v in ngram_dict.items()}
    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white",font_path=font_path).generate_from_frequencies(ngram_freq)
    
    # Plot the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title, fontsize=20)
    plt.show()
# Function to calculate the conditional probabilities for bigrams
def calculate_conditional_probabilities(ngram_dict):
    # Step 1: Calculate the frequency of the first word in each bigram
    word_count = defaultdict(int)
    # Count the occurrences of each word as the first word of a bigram
    for bigram, count in ngram_dict.items():
        first_word = bigram[0]
        word_count[first_word] += count
    
    # Step 2: Calculate the conditional probabilities
    conditional_probabilities = {}
    for bigram, bigram_count in ngram_dict.items():
        first_word = bigram[0]
        # Conditional probability P(w2 | w1) = Count(w1, w2) / Count(w1)
        conditional_prob = bigram_count / word_count[first_word]
        conditional_probabilities[bigram] = conditional_prob
    
    return conditional_probabilities
# create ngrams 1,2,3,4....
def remove_stop_words(words,stop_words):
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)
def calculate_n_grams(n): 
 for i in range(1,n+1) : 
    ngrams=generate_ngrams(tokens,i)
    print_ngram(ngrams,i)
# calculates top k probabilitise for n=1,2,3,4....
def calculate_top_probabilties_for_n(tokens,n,top_k=10):
    for i in range(1,n+1) : 
        ngrams_dict=generate_ngrams(tokens,i)
        ngram_probabilities=calculate_ngram_probabilities(ngrams_dict)
        top_k_probabilites=find_top_ngrams_by_proability(ngram_probabilities)
        print_ngram(top_k_probabilites,i)
def calculate_top_frequency_for_n(tokens,n,top_k=10):
    for i in range(1,n+1) : 
        ngrams_dict=generate_ngrams(tokens,i)
        top_k_frequency=find_top_ngrams_by_frequency(ngrams_dict,top_k)
        print_ngram(top_k_frequency,i) 
def split_train_test_data(tokens,chunk_size):
    # corpus_length = len(corpus)
    # Create chunks
    # Step 3: Split the words into chunks of a fixed number of words (e.g., 3 words per chunk)
    chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]
        
    #  Shuffle the chunks to ensure randomness
    random.shuffle(chunks)
    # Split 80% training, 20% testing
    train_size = int(0.8 * len(chunks))  # 80% for training
    train_set = chunks[:train_size]
    test_set = chunks[train_size:]
    # Join chunks back into strings (if needed)
    train_data = ''.join(train_set)
    test_data = ''.join(test_set)
    return train_data,test_data

# Function to generate a random sentence based on n-grams
def generate_random_sentence(ngram_probabilities, n, max_length=10):
    # Choose a random starting n-gram
    current_ngram = random.choice(list(ngram_probabilities.keys()))
    sentence = list(current_ngram)
    
    while len(sentence) < max_length:
        # Generate the next word based on the last n-1 words
        possible_next_words = [ngram[-1] for ngram in ngram_probabilities.keys() if ngram[:-1] == tuple(sentence[-(n-1):])]
        
        if not possible_next_words:
            break  # If no continuation is found, stop generating
        
        next_word = random.choice(possible_next_words)
        sentence.append(next_word)
    
    return ' '.join(sentence)

# question 1.1
# calculate_n_grams(number_of_grams)
# question 1.2
# calculate_top_probabilties_for_n(number_of_grams)
# question 1.3
# bi_grams=2
# bi_gram_dic=generate_ngrams(tokens,bi_grams)
# condtional_probabilities=calculate_conditional_probabilities(bi_gram_dic)
# pring_bigram_condtional_probabilities(condtional_probabilities,bi_grams)
# question 1.4
num_of_grams=2
stop_words = {
    "እኔ", "የእኔ", "እኔ ራሴ", "እኛ", "የእኛ", "የእኛ", 
    "እኛ ራሳችን", "አንቺ", "ያንተ", "ራስህን", "እራሳችሁ", 
    "እሱ", "የእሱ", "ራሱ", "እሷ", "የእሷ", "እራሷ", 
    "እነሱ", "እነሱን", "የእነሱ", "ራሳቸው", "ምንድን", 
    "የትኛው", "የአለም ጤና ድርጅት", "ማን", "ይህ", 
    "የሚል ነው", "እነዚህ", "እነዚያ", "ነኝ", "ነው", 
    "ናቸው", "ነበር", "ነበሩ", "ሁን", "ቆይቷል", 
    "መሆን", "አላቸው", "አለው", "ነበረው", "ያለው", 
    "መ ስ ራ ት", "ያደርጋል", "አደረገ", "ማድረግ", 
    "አንድ", "የ", "እና", "ግን", "ከሆነ", "ወይም", 
    "ምክንያቱም", "እንደ", "እስከ", "እያለ", "የ", 
    "ለ", "ጋር", "ስለ", "ላይ", "መካከል", "ወደ", 
    "በኩል", "ወቅት", "ከዚህ በፊት", "በኋላ", 
    "ከላይ", "ከታች", "ወደከ", "ወደ ላይ", "ታች", 
    "ውስጥ", "ውጭ", "ላይ", "ጠፍቷል", "በላይ", 
    "በታች", "እንደገና", "ተጨማሪ", "ከዚያ", 
    "አንድ ጊዜ", "እዚህ", "እዚያ", "መቼ", "የት", 
    "እንዴት", "እንዴት", "ሁሉም", "ማንኛውም", 
    "ሁለቱም", "እያንዳንዳቸው", "ጥቂቶች", "ተጨማሪ", 
    "በጣም", "ሌላ", "አንዳንድ", "እንደዚህ", 
    "አይ", "ወይም አይደለም", "አይደለም", "ብቻ", 
    "የራሱ", "ተመሳሳይ", "ስለዚህ", "ይልቅ", 
    "እንዲሁ", "በጣም", "እ.ኤ.አ.", "ት", 
    "ይችላል", "ያደርጋል", "ብቻ", "ዶን", "ይገባል", "አሁን"
}
stopword_removed_text = remove_stop_words(tokens,stop_words)
# tokens=stopword_removed_text.split()

# print(stopword_removed_text)

# calculate_top_frequency_for_n(tokens,num_of_grams)

# Question 1.5 
# before removing stopwords 
# unigram_dic=generate_ngrams(tokens,1)
# bigram_dic=generate_ngrams(tokens,2)
# # trigram_dic=generate_ngrams(tokens,3)
# create_wordcloud(bigram_dic,"bigram")
# Question 1.6
# Define n for n-gram model
# n = 3  # Bigram model

# # Build the n-gram probabilities for the entire corpus
# ngram_probabilities = build_corpus_ngram_probabilities(tokens, n)

# # Example sentence to calculate its probability (also tokenized)
# sentence = "ኢትዮጵያ ታሪካዊ ሀገር ናት"
# tokenized_sentence=sentence.split()

# # Calculate the probability of the sentence using n-gram probabilities from the corpus
# sentence_probability = calculate_sentence_probability(tokenized_sentence, ngram_probabilities, n)
# print(f"Probability of the sentence: {sentence_probability}")

# Question 1.7
# Generate unigrams, bigrams, and trigrams
# unigram_probabilities = generate_ngrams(tokens, 1)
# bigram_probabilities = generate_ngrams(tokens, 2)
# trigram_probabilities = generate_ngrams(tokens, 3)
gram_4_probabilities=generate_ngrams(tokens, 4)

# Generate random sentences using unigrams, bigrams, and trigrams
# print("Random sentence using Unigrams:")
print(generate_random_sentence(unigram_probabilities, 1))

# print("\nRandom sentence using Bigrams:")
# print(generate_random_sentence(bigram_probabilities, 1))

# print("\nRandom sentence using 4-gram:")
# print(generate_random_sentence(gram_4_probabilities, 1))
# train_data,test_data=split_train_test_data(tokens,10)
# print("======train data====\n",train_data)
# print("=======test data=======\n",test_data)