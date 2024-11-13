# Open the file and read the first few lines
with open('dataset/GPAC.txt', 'r') as file:
    # Read the first 10 lines one by one (adjust the number as needed)
    for i, line in enumerate(file):
        if i >= 3:  # Stop after reading 10 lines
            break
        print(line.strip())  # Print each line, removing extra newlines