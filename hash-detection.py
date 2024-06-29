import os
import shutil
import zipfile
import hashlib
from rarfile import RarFile

def print_directory_contents(directory):
    print(f"Contents of directory {directory} : ")
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(os.path.join(root, file))
        for dir in dirs:
            print(os.path.join(root, dir))

def zip_file(file_path, output_zip_file):
    with zipfile.ZipFile(output_zip_file, 'w', zipfile.ZIP_DEFLATED) as zip:
        zip.write(file_path, os.path.basename(file_path))
    print(f"File {file_path} zipped successfully to {output_zip_file}.")

def unzip_file(zip_file_path, output_directory):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(output_directory)
    print(f"Files extracted successfully to {output_directory}.")
    print_directory_contents(output_directory)

def zip_directory(source_directory, output_filename):
    shutil.make_archive(output_filename, 'zip', source_directory)
    print(f"Directory {source_directory} has been zipped to {output_filename}.zip")

def unzip_directory(zip_dir_path, output_directory):
        if zip_dir_path.lower().endswith('.zip'):
            with zipfile.ZipFile(zip_dir_path, 'r') as zip_dir:
                zip_dir.extractall(output_directory)
            print(f"Files extracted successfully to {output_directory}.")
        elif zip_dir_path.lower().endswith('.rar'):
            with RarFile(zip_dir_path, 'r') as rar_file:
                rar_file.extractall(output_directory)
            print(f"Files extracted successfully to {output_directory}.")
        else:
            print(f"Unsupported file format: {zip_dir_path}")
        print_directory_contents(output_directory)

def hasH_func(input_file, hash):
    try:
        with open(input_file, 'rb') as opened_file:
            read_file = opened_file.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        exit()

    print(f"\nHashes for file: {input_file}")
    found_match = False
    for algo in hashlib.algorithms_guaranteed:
        hash_func = getattr(hashlib, algo)
        if algo.startswith('shake'):
            hash_value = hash_func(read_file).hexdigest(64)
        else:
            hash_value = hash_func(read_file).hexdigest()
        print(f"{algo.upper()} : {hash_value}")
        if input_hash == hash_value:
            print(f"Match found: {algo.upper()} hash is a match for the given hash.")
            found_match = True
            break
    if not found_match:
        print("No matching hash found.")

while True:
    cho_dir_file = input("Do you want to work with a file or directory? (file/dir/hash): ").lower()

    if cho_dir_file == 'file':
        choo_se = input("Do you want to make a Zip or Unzip? (zip/unzip): ").lower()

        if choo_se == 'zip':
            file_path = input("Enter the path to the file you want to zip: ")
            if os.path.exists(file_path):
                output_zip_file = input("Enter the path for the output ZIP file: ")
                zip_file(file_path, output_zip_file)
            else:
                print(f"The file {file_path} does not exist.")

        elif choo_se == 'unzip':
            zip_file_path = input("Enter the path to the ZIP file you want to unzip: ")
            if os.path.exists(zip_file_path):
                output_directory = input("Enter the path to the directory where you want to extract the files: ")
                unzip_file(zip_file_path, output_directory)
            else:
                print(f"The file {zip_file_path} does not exist.")

        else:
            print("Sorry, you didn't choose correctly. Please try again.")

    elif cho_dir_file == 'dir':
        choo_se_dir = input("Do you want to make a Zip or Unzip? (zip/unzip): ").lower()
        
        if choo_se_dir == 'zip':
            source_directory = input("Enter the path to the directory you want to zip: ")
            if os.path.exists(source_directory):
                output_dir_name = input("Enter the path for the output ZIP file (without extension): ")
                zip_directory(source_directory, output_dir_name)
            else:
                print(f"The source directory {source_directory} does not exist.")

        elif choo_se_dir == 'unzip':
            zip_dir_path = input("Enter the path to the ZIP file you want to unzip: ")
            if os.path.exists(zip_dir_path):
                output_directory = input("Enter the path to the directory where you want to extract the files: ")
                unzip_directory(zip_dir_path, output_directory)
            else:
                print(f"The file {zip_dir_path} does not exist.")
    
    elif cho_dir_file == 'hash':
        input_file = input("Enter The file To See all hash avaliable : ")
        input_hash = input("Enter your Hash you hava and will return by Match or not : ")
        hasH_func(input_file, input_hash)
    
    else:
            print("Sorry, you didn't choose correctly. Please try again.")

