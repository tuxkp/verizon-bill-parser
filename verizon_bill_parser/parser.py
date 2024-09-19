import os

def parse():
    return "Hello, world!"

def parse_directory(directory: str):
    resp_list = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            resp_list.append((filename, file_size))
    return resp_list