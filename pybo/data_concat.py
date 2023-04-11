import os

def handle_uploaded_file(f):
    with open(os.path.join('media/data_concat/', f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def delete_files_in_directory(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except:
            pass