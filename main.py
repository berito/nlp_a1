from nltk.translate.bleu_score import sentence_bleu
from tokenizer import Tokenizer
from corpus_spliter import CorpusSplitter
from ngram import NGram
from ngram_model import NgramModel
from utils import hdf5_data_loader,stop_word_reader,calculate_sentence_probability
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

def sentence_probability():
    # sentence ngram
    # sentence = ['ኢትዮጵያ ታሪካዊ ሀገር ናት']
    sentence = ['መረባረብ ነው ስለዚህ ደርግም']
    sentence_tokenizer=Tokenizer(sentence)
    sentence_tokens=sentence_tokenizer.tokenize(remove_punctuation=True)
    NGram.tokens=sentence_tokens
    sentence_gram_4=NGram(4)
    sentence_gram_4.generate()
    # print(sentence_gram_4.get_ngrams())
    # print(sentence_gram_4.probabilities())
    NGram.tokens=tokens
    gram_4=NGram(4)
    gram_4.generate()
    # print(gram_4.probabilities())
    probability=calculate_sentence_probability(sentence_gram_4,gram_4)
    print(f'probability of {sentence} is {probability:.7f}')
    
   
def compare_ngrams_wordcount():
    n=4
    # before
    print(len(tokens))
    create_n_gram(n,tokens,"4-gram")
    # after
    tokens = tokenizer.tokenize(remove_punctuation=True,stop_words=stop_words)
    print(len(tokens))
    create_n_gram(n,tokens,"4-gram")
    # stop_word_reader_test()

def create_n_gram(n,tokens,title):
    # Create an NGram instance
    NGram.tokens=tokens
    gram_4=NGram(n)
    gram_4.generate()
    # ngram.display()
    gram_4.create_wordcloud(title)
    # Calculate probabilities
    # print("\nProbabilities:")
    # probabilities = ngram.probabilities()
    # for ngram_tuple, prob in probabilities.items():
    #     print(f"{' '.join(ngram_tuple)}: {prob:.4f}")
    # Display conditional probabilities
    # print("\nConditional Probabilities:")
    # ngram.display_conditional_probabilities()
    # # Get top 5 frequencies
    # print("\nTop 5 Frequencies:")
    # top_ngrams = ngram.top_frequencies(40)
    # for ngram_tuple, freq in top_ngrams:
    #     print(f"{' '.join(ngram_tuple)}: {freq}")

def sentence_generator():
    NGram.tokens=tokens
    gram=NGram(4)
    gram.generate()
    rand_sentence=gram.generate_random_sentence(4)
    print(rand_sentence)    

def corpus_splitter_test():
     # print(len(tokens))
    corpus_splitter = CorpusSplitter(corpus, split_ratio=0.8, random_seed=42)
    # # Split the corpus into training and testing sets
    train_set, test_set = corpus_splitter.split()
    print("==================training set================= ",len(train_set))
    print(train_set)
    print("==================training set================= ",len(train_set))
    print(test_set)
    # # Output the results
    # print("Training Set:", len(train_set.split()))
    # print("Test Set:", len(test_set.split()))
def stop_word_reader_test():
    file_path='stopwords_am.txt'
    stop_words=stop_word_reader(file_path)
    print(stop_words)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read text from an HDF5 file and display a specific number of characters.")
    parser.add_argument('--chunk_size', type=int, default=500, help="Number of words or sentence from the text.")
    args = parser.parse_args()
    chunk_size = args.chunk_size
    total_chunks,corpus,next=hdf5_data_loader(chunk_size)
    print(f'total chunk size',total_chunks)
    print(f'total number of sentence (total_chunks*10(sentence per chunk)',total_chunks*10)
    print(f'Retrived number of sentence )',chunk_size*10)
    stop_words_file_path = 'stopwords_am.txt'
    stop_words = stop_word_reader(stop_words_file_path)
    tokenizer = Tokenizer(corpus) 
    tokens = tokenizer.tokenize(remove_punctuation=True)
    # print(tokens)
    # len_before=len(tokens)
    # print('before stop word removed',len_before)
    # tokens = tokenizer.tokenize(remove_punctuation=True,stop_words=stop_words)
    # len_after=len(tokens)
    # print('after stop word removed',len_after)
    # print("difference ",len_before-len_after)
    corpus_splitter = CorpusSplitter(corpus,stopwords=stop_words, split_ratio=0.8, random_seed=42)
    # # Split the corpus into training and testing sets
    train_set, test_set = corpus_splitter.split()
    # corpus_splitter = CorpusSplitter(corpus, split_ratio=0.8, random_seed=42)
    # train_set, test_set = corpus_splitter.split()
    # print("==================training set================= ",len(train_set))
    # print(len(train_set))
    # print("==================test set================= ",len(test_set))
    # print(test_set)

    model=NgramModel(n=4,alpha=1)
    model.train(train_set)
    # # perplexity = model.perplexity(test_set)
    # # print(f"Perplexity: {perplexity:.2f}")
    
    # # Reference text from corpus
    reference = ["ፊቱ" "ምንም" "ድካምም" "ሆነ" "መሰልቸት" "አይታይበትም"]
    # # Train the model
  
  

    # Generate text
    generated_text = model.generate(max_words=20)
    print("Generated Text:", generated_text)
    candidate = generated_text.split()

    # Compute BLEU score
    bleu_score = sentence_bleu(reference, candidate)
    print(f"BLEU Score: {bleu_score}")