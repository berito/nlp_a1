import h5py  
def read_hd5(num_chars):       
    # Open the HDF5 file to read the text data and metadata
    with h5py.File('dataset/GPAC_data.h5', 'r') as hdf:
        # Access the scalar dataset containing the text content
        text_data = hdf['text_data'][()]  # Directly access the scalar dataset (use [()] to retrieve the value)
        
        # Decode the text from bytes to string
        decoded_text = text_data.decode('utf-8')

        # Access the metadata (attributes)
        num_chars_in_text = hdf.attrs.get('num_chars', 'Metadata not found')
       
    return (decoded_text[:num_chars], num_chars_in_text)
def get_text_by_words(num_words):
    with h5py.File('dataset/GPAC_data.h5', 'r') as hdf:
        # Access the scalar dataset containing the text content
        text_data = hdf['text_data'][()]  # Directly access the scalar dataset (use [()] to retrieve the value) 
        # Decode the text from bytes to string
        decoded_text = text_data.decode('utf-8')
        words = decoded_text.split()
        words_subset = words[:num_words]
        words_text = ' '.join(words_subset)
        return words_text, len(words)
