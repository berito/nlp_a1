import h5py
import re

input_file = 'dataset/GPAC.txt'  # Input text file
output_file = 'dataset/GPAC_data_chunk.h5'  # Output HDF5 file
sentences_per_chunk=10
def save_file_as_scalar():
    # Define the input and output file paths
    input_file = 'dataset/GPAC.txt'  # Input text file
    output_file = 'dataset/GPAC_data.h5'  # Output HDF5 file

    # Read the content of the text file and count characters
    with open(input_file, 'r', encoding='utf-8') as infile:
        content = infile.read()  # Read the entire file content as a single string
        num_chars = len(content)  # Total number of characters (including spaces and newlines)

    # Create an HDF5 file and write the content as a scalar dataset
    with h5py.File(output_file, 'w') as hdf:
        # Store the content as a single string (scalar dataset)
        hdf.create_dataset('text_data', data=content.encode('utf-8'))  # Encoding the content as bytes
        
        # Store the metadata (attributes)
        hdf.attrs['num_chars'] = num_chars  # Total number of characters

    print(f"Text file has been successfully converted to HDF5 format and saved to {output_file}")
    print(f"Number of characters: {num_chars}")

def get_sentences(content):
       # split sentence using sentence separator like ::
        sentences = re.split(r'(፡፡|፡|።)\s*', content)
        # Remove '፡፡'
        sentences = [re.sub(r'፡፡', '', sentence) for sentence in sentences] 
        # First, filter out empty sentences
        sentences = [sentence for sentence in sentences if sentence.strip()]
        # Then, remove extra spaces within each sentence and strip leading/trailing spaces
        sentences = [re.sub(r'\s+', ' ', sentence).strip() for sentence in sentences]
        return sentences

def save_sentences_in_chunks():
    # Read the content of the input file
    with open(input_file, 'r', encoding='utf-8') as infile:
        content = infile.read()  # Read the entire file content as a single string
    sentences=get_sentences(content)
    # print(sentences[:6])
    # Group sentences into chunks (each chunk will have `sentences_per_chunk` sentences)
    chunks = [sentences[i:i+sentences_per_chunk] for i in range(0, len(sentences), sentences_per_chunk)]
    
    # Create an HDF5 file to store the data
    with h5py.File(output_file, 'w') as hdf:
        # Create a dataset for storing sentence chunks
        dtype = h5py.string_dtype(encoding='utf-8')  # Use UTF-8 encoding for the sentences
        max_shape = (None,)  # Unlimited size for dynamic growth
        chunk_shape = (1,sentences_per_chunk)  # Define chunk size (number of sentences per chunk)
        
        dataset = hdf.create_dataset('text_data', 
                                     shape=(len(chunks), sentences_per_chunk),  # Number of chunks and sentences per chunk
                                     dtype=dtype,  # Use the string dtype for encoding UTF-8 strings
                                     maxshape=(None, sentences_per_chunk),  # Unlimited size along the first axis
                                     chunks=chunk_shape,#(1, sentences_per_chunk),  # Chunking along the first axis (1 chunk at a time)
                                     compression="gzip")  #
        # Write each chunk of sentences into the dataset
        for i, chunk in enumerate(chunks):
            dataset[i] = chunk

    print(f"Text data has been stored in {output_file} with sentence chunks.")

save_sentences_in_chunks()

 
