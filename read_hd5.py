import h5py
import argparse

# Set up argument parsing to accept the number of characters as a command-line argument
parser = argparse.ArgumentParser(description="Read text from an HDF5 file and display a specific number of characters.")
parser.add_argument('--num_chars', type=int, default=500, help="Number of characters to display from the text.")
args = parser.parse_args()

# Open the HDF5 file to read the text data and metadata
with h5py.File('dataset/GPAC_data.h5', 'r') as hdf:
    # Access the scalar dataset containing the text content
    text_data = hdf['text_data'][()]  # Directly access the scalar dataset (use [()] to retrieve the value)
    
    # Decode the text from bytes to string
    decoded_text = text_data.decode('utf-8')

    # Access the metadata (attributes)
    num_chars_in_text = hdf.attrs.get('num_chars', 'Metadata not found')

    # Print the metadata (total number of characters in the text)
    print(f"Total number of characters in the text: {num_chars_in_text}")

    # Print the specified number of characters (from the argument)
    print(f"\nFirst {args.num_chars} characters of the content:")
    print(decoded_text[:args.num_chars])  # Print the specified number of characters

