import pandas as pd
import csv
import os
import sqlite3
import re
import concurrent.futures
import sys

file_extensions = [".csv", ".xlsx", ".xls", ".tsv",
                   ".parquet", ".feather", ".sqlite", ".db"]
csv_folder = os.path.join(sys.argv[-1], 'csvs')


def clean_file_name(file_name):
    return re.sub(r'[^\w\-_.]', '', file_name).replace(' ', '_')


def get_unique_csv_file_name(file_path):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    folder_name = os.path.basename(os.path.dirname(file_path))
    counter = 1
    unique_file_name = f"{clean_file_name(folder_name)}_{clean_file_name(base_name)}.csv"

    while os.path.exists(os.path.join(csv_folder, unique_file_name)):
        unique_file_name = f"{clean_file_name(folder_name)}_{clean_file_name(base_name)}_{counter}.csv"
        counter += 1

    return unique_file_name


def export_table_to_csv(database_file, table_name):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    csv_file = os.path.join(csv_folder, get_unique_csv_file_name(f'{os.path.basename(database_file)}_{table_name}.csv'))
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        column_names = [description[0] for description in cursor.description]
        csv_writer.writerow(column_names)
        csv_writer.writerows(rows)

    print(f'Table "{table_name}" exported to "{csv_file}" successfully.')
    conn.close()

def process_csv_file(file_input):
    file_name = os.path.splitext(os.path.basename(file_input))[0]
    parent_folder = os.path.basename(os.path.dirname(file_input))
    for extension in file_extensions:
        if file_input.endswith(extension):
            try:
                if extension == ".csv":
                    if is_file_empty(file_input):
                        print(f"CSV file '{file_input}' is empty. Skipping conversion.")
                        return
                    df = pd.read_csv(file_input)
                    print("Read CSV file as DataFrame")

                elif extension == ".xlsx" or extension == ".xls":
                    xls = pd.ExcelFile(file_input)
                    for sheet_name in xls.sheet_names:
                        dataframe = xls.parse(sheet_name)
                        csv_filename = f"{clean_file_name(parent_folder)}_{clean_file_name(file_name)}_{clean_file_name(sheet_name)}.csv"
                        csv_path = os.path.join(csv_folder, get_unique_csv_file_name(csv_filename))
                        dataframe.to_csv(csv_path, index=False)
                        print(
                            f"Sheet '{sheet_name}' converted and saved as '{csv_filename}'.")
                    break

                elif extension == ".tsv":
                    if is_file_empty(file_input):
                        print(f"CSV file '{file_input}' is empty. Skipping conversion.")
                        return
                    df = pd.read_csv(file_input, delimiter='\t')
                    print("Read TSV file as DataFrame")

                elif extension == ".parquet":
                    df = pd.read_parquet(file_input)
                    print("Read Parquet file as DataFrame")

                elif extension == ".feather":
                    df = pd.read_feather(file_input)
                    print("Read Feather file as DataFrame")

                elif extension == ".sqlite" or extension == ".db":
                    conn = sqlite3.connect(file_input)
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT name FROM sqlite_master WHERE type='table'")
                    tables = cursor.fetchall()
                    for table in tables:
                        table_name = table[0]
                        export_table_to_csv(file_input, table_name)
                    conn.close()
                    break

                csv_filename = f"{clean_file_name(parent_folder)}_{clean_file_name(file_name)}.csv"
                csv_path = os.path.join(csv_folder, get_unique_csv_file_name(csv_filename))
                df.to_csv(csv_path, index=False)
                print(
                    f"File converted and saved as '{csv_path}' in '{csv_folder}' folder.")
            except AttributeError:
                print(
                    f"No command available in pandas to read {extension} files.")
            break
    else:
        print("Invalid file extension.")

def convert_to_csv_parallel(file_input):
    csv_folder = os.path.join(sys.argv[-1], 'csvs')
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    if os.path.isdir(file_input):
        # If the input is a directory, process all files in the directory in parallel
        files = [os.path.join(file_input, f) for f in os.listdir(file_input)]
    else:
        # If the input is a single file, process only that file
        files = [file_input]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(process_csv_file, file): file for file in files}

        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
            try:
                future.result()
            except Exception as exc:
                print(f"Error processing file {file}: {exc}")


def is_file_empty(file_path):
    with open(file_path) as f:
        first_line = f.readline().strip()
        return not first_line