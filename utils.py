import h5py 
def read_stop_words(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            stop_words = {line.strip() for line in file if line.strip()}
        return stop_words
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return set()  # Return an empty set if the file is not found
    except Exception as e:
        print(f"Error reading stop words: {e}")
        return set()
def hdf5_data_loader():
    with h5py.File('dataset/GPAC_data.h5', 'r') as hdf:
        text_data = hdf['text_data'][()]  # Access the text data
        return text_data.decode('utf-8')  # Decode the text from bytes to string