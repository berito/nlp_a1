import h5py 
def stop_word_reader(file_path):
    try:
       with open(file_path, 'r', encoding='utf-8') as file:
            # Parse and clean stop words into a list
            stop_words = [
                word.strip().strip('"')  # Remove whitespace and quotes
                for line in file
                for word in line.split(',')  # Split by commas
                if word.strip()  # Ignore empty words
            ]
       return stop_words
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return []  # Return an empty list if the file is not found
    except Exception as e:
        print(f"Error reading stop words: {e}")
        return []  # Return an empty list in case of any other exception
def hdf5_data_loader_old():
    with h5py.File('dataset/GPAC_data.h5', 'r') as hdf:
        text_data = hdf['text_data'][()]  # Access the text data
        return text_data.decode('utf-8')  # Decode the text from bytes to string
def hdf5_data_loader(chunk_size, start_index=0):
    file_path = 'dataset/GPAC_data.h5'
    dataset_name = 'text_data'
    
    with h5py.File(file_path, 'r') as hdf:
        dataset = hdf[dataset_name]
        
        # Ensure the dataset is valid and check its shape
        if isinstance(dataset, h5py.Dataset):
            if hasattr(dataset, 'shape'):
                # In this case, the shape will be (num_chunks, sentences_per_chunk)
                total_chunks = dataset.shape[0]  # Number of chunks in the dataset
                sentences_per_chunk = dataset.shape[1]  # Sentences per chunk (e.g., 10 sentences)
            else:
                raise ValueError(f"Dataset '{dataset_name}' does not have a shape attribute.")
        else:
            raise TypeError(f"Dataset '{dataset_name}' is not a valid h5py.Dataset.")
        
        # Calculate the end index, making sure it's within bounds
        end_index = min(start_index + chunk_size, total_chunks)
        
        # Read the chunk of data (in this case, we are selecting rows from the first dimension)
        chunk_data = dataset[start_index:end_index]  # This retrieves a chunk of sentences
        
        # Flatten the chunk data if you want to read sentence-by-sentence
        # You can also choose to read smaller chunks from the existing 10-sentence chunks
        chunk_data_decoded = []
        
        for chunk in chunk_data:
            # Read only the first 2 sentences per chunk or any subset of sentences
            chunk_data_decoded.extend([sentence.decode('utf-8') for sentence in chunk[:chunk_size]])

        # Return the decoded chunk data and the new end index
        return total_chunks,chunk_data_decoded, end_index
