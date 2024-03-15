import pandas as pd

# Function to convert the text file to CSV
def convert_text_to_csv(input_file, output_file):
    # Initialize lists to hold file names and labels
    fnames = []
    labels = []
    
    # Open and read the input file
    with open(input_file, 'r') as file:
        for line in file:
            # Split each line into filename and label parts
            parts = line.strip().split('\t')
            if len(parts) >= 2:  # Ensure there are at least two parts
                # Append filename and label (concatenated with space) to the lists
                fnames.append(parts[0])
                labels.append(parts[1] + ' ' + parts[2])

    # Create a DataFrame from the lists
    df = pd.DataFrame({'fname': fnames, 'labels': labels})

    # Write the DataFrame to a CSV file
    df.to_csv(output_file, index=False)

# Usage of the function
input_file = 'labels.txt'  # Replace 'your_input_file.txt' with your actual input file path
output_file = 'train.csv'           # The desired output file name

# Convert the file
convert_text_to_csv(input_file, output_file)
