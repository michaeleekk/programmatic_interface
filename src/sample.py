
import uuid

class Sample:
    def __init__(self, experiment_id, sample_obj):
        self.__sample_obj = sample_obj
        self.__experiment_id = experiment_id
        self.__uuid = uuid.uuid4()
    
    def to_json(self):
        return {
            'name': self.__sample_obj['name'],
            'sampleTechnology': '10x'
        }

    def uuid(self):
        return self.__uuid

    def experiment_id(self):
        return self.__experiment_id

    def get_sample_files(self):
        return [
            self.SampleFile(sample_file) for sample_file in self.__sample_obj['sample_files']
        ]
        
    class SampleFile:
        def __init__(self, file):
            self.__file = file

        def type(self):
            return self.__file.type()

        def to_json(self):
            return {
                'sampleFileId': str(uuid.uuid4()),
                'size': self.__file.size(),
                "metadata": {},
            }