import csv
import os

input_folder = 'tbls/'
output_folder = 'csvs/'

# Iterate over each file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.tbl'):
        tbl_file = os.path.join(input_folder, filename)
        csv_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.csv")

        # Open the .tbl file for reading
        with open(tbl_file, 'r') as tbl:
            # Open the CSV file for writing
            with open(csv_file, 'w', newline='') as csvf:
                writer = csv.writer(csvf)

                # Iterate over each line in the .tbl file
                for line in tbl:
                    # Remove leading and trailing whitespace and split the line by the field separator
                    fields = line.strip().split('|')

                    # Write the fields as a row in the CSV file
                    writer.writerow(fields)
