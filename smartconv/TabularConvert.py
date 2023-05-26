import pandas as pd
import csv
import os
import json
import sqlite3

file_extensions = [".csv", ".xlsx", ".xls", ".tsv",
                   ".parquet", ".feather", ".sqlite", ".db"]
csv_folder = 'csvs'

def export_table_to_csv(database_file, table_name):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    csv_file = os.path.join(csv_folder, f'{os.path.splitext(database_file)[0]}_{table_name}.csv')
    csv_file = csv_file.lstrip('/')  # Remove leading forward slash
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        column_names = [description[0] for description in cursor.description]
        csv_writer.writerow(column_names)
        csv_writer.writerows(rows)

    print(f'Table "{table_name}" exported to "{csv_file}" successfully.')
    conn.close()



def convert_to_csv_s(file_input):
    file_name = os.path.splitext(file_input)[0]
    print("File name: ",file_name)
    output_file = f"{file_name}.csv"
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)
    csv_path = os.path.join(csv_folder, output_file)
    for extension in file_extensions:
        if file_input.endswith(extension):
            try:
                if extension == ".csv":
                    df = pd.read_csv(file_input)
                    print("Read CSV file as DataFrame")
                elif extension == ".xlsx" or extension == ".xls":
                        xls = pd.ExcelFile(file_input)
                        for sheet_name in xls.sheet_names:
                            dataframe = xls.parse(sheet_name)
                            csv_filename = f"{sheet_name}.csv"
                            dataframe.to_csv(csv_filename, index=False)
                            print(f"Sheet '{sheet_name}' converted and saved as '{csv_filename}'.")
                        break
                elif extension == ".tsv":
                    df = pd.read_csv(file_input, delimiter='\t')
                    print("Read TSV file as DataFrame")
                # elif extension == ".dat":
                #     with open(file_input, 'r') as file:
                #         dialect = csv.Sniffer().sniff(file.read(1024))
                #         delimiter = dialect.delimiter
                #     df = pd.read_csv(file_input, delimiter=delimiter)
                #     print("Read .dat file as DataFrame")
                # elif extension == ".dbf":
                #     table = DBF(file_input)
                #     df = pd.DataFrame(iter(table))
                #     print("Read .dbf file as DataFrame")
                elif extension == ".parquet":
                    df = pd.read_parquet(file_input)
                    print("Read Parquet file as DataFrame")
                elif extension == ".feather":
                    df = pd.read_feather(file_input)
                    print("Read Feather file as DataFrame")
                # elif extension == ".h5" or extension == ".hdf5":
                #     df = pd.read_hdf(file_input)
                #     print("Read HDF5 file as DataFrame")
                elif extension == ".sqlite" or extension == ".db":
                    conn = sqlite3.connect(file_input)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = cursor.fetchall()
                    for table in tables:
                        table_name = table[0]
                        export_table_to_csv(file_input, table_name)
                    conn.close()
                    break

                df.to_csv(csv_path, index=False)
            except AttributeError:
                print(f"No command available in pandas to read {extension} files.")
            break
    else:
        print("Invalid file extension.")


