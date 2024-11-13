import h5py

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

