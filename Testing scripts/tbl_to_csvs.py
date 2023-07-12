import csv
import os
import random
import string
from multiprocessing.dummy import Pool

input_folder = 'data/'
output_folder = 'csvs/'

# Number of threads to use
num_threads = 4

# Function to process a file
def process_file(filename):
    if filename.endswith('.tbl'):
        tbl_file = os.path.join(input_folder, filename)
        csv_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.csv")

        # Remove commas and trailing '|' from the .tbl file and store the contents in a list
        tbl_data = []
        with open(tbl_file, 'r') as tbl:
            for line in tbl:
                line = line.replace(',', '')  # Remove commas
                line = line.rstrip('\n|')  # Remove trailing '|' and newline characters
                tbl_data.append(line.strip())


        # Get the number of columns from the first row of data
        first_row_fields = tbl_data[0].split('|')
        num_columns = len(first_row_fields)

        # Generate random column headers
        column_headers = [f'Column_{i+1}' for i in range(num_columns)]

        # Write the data to the CSV file with the random headers
        with open(csv_file, 'w', newline='') as csvf:
            writer = csv.writer(csvf)

            # Write the column headers
            writer.writerow(column_headers)

            # Write the data rows
            for line in tbl_data:
                fields = line.split('|')
                writer.writerow(fields)

# List files in the input folder
files = os.listdir(input_folder)

# Create a pool of worker threads
pool = Pool(num_threads)

# Process the files using the pool of threads
pool.map(process_file, files)

# Close the pool of threads and wait for them to finish
pool.close()
pool.join()

print('Conversion to CSV completed.')
