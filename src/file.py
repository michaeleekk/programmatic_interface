from os.path import isfile, join, getsize
from os import listdir

class File:
    def __init__(self, path):
        self.__path = path

    def path(self):
        return self.__path

    def name(self):
        return self.__path.split('/')[-1]

    def folder(self):
        return self.__path.split('/')[-2]

    def size(self):
        return getsize(self.__path)

    def type(self): 
        file_types = {
            'matrix': 'matrix10x',
            'barcodes': 'barcodes10x',
            'features': 'features10x',
            'genes': 'features10x',
        }

        for file_type_key in file_types.keys():
            if file_type_key in self.name():
                return file_types[file_type_key]
        return None

    @staticmethod
    def get_files(path): 
        file_paths = listdir(path)

        ret = {}
        for file_path in file_paths:
            full_path = join(path, file_path)

            if isfile(full_path):
                file = File(full_path)
                folder_name = file.folder()
    
                if ret.get(folder_name) == None:
                    ret[folder_name] = {
                        'name': folder_name,
                        'sample_files': [file],
                        'full_path': path
                    }
                else:
                    ret[folder_name]['sample_files'].append(file)
                continue

            ret.update(File.get_files(full_path))

        return ret