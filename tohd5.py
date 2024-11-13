import h5py

# # Open an HDF5 file for writing
# with h5py.File('dataset/text_data.h5', 'w') as f:
#     # Store the text data in the HDF5 file as a dataset
#     with open('dataset/GPAC.txt', 'r', encoding='utf-8') as file:
#         data = file.readlines()
#         f.create_dataset('text_data', data=data)

# Read the data from the HDF5 file
with h5py.File('dataset/text_data.h5', 'r') as f:
    data = f['text_data'][:]
    print(data[:10])  # Print the first 10 lines
