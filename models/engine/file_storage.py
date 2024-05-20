#!/usr/bin/python3
"""Define the fileStorage file
"""

import json
from models.base_model import BaseModel

class FileStorage:
    """An abstract storage engine in json

    Attributes:
        __file_path (str): path to json file
        __objects (dict): store objects of a class
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects
        """
        return self.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id
        """
        objname = obj.__class__.__name__
        objid = obj.id
        self.__objects["{}.{}".format(objname, objid)] = obj
    
    def save(self):
        """serializes __objects to the JSON file (path: __file_path)
        """

        new_dict = {}

        for key in self.__objects.keys():
            new_dict[key] = self.__objects[key].to_dict()

        with open(self.__file_path, "w") as file:
            file.write(json.dumps(new_dict))

    def reload(self):
        """deserializes the JSON file to __objects (only if the JSON file (__file_path) exists ; otherwise, do nothing
        """
        try:
            with open(self.__file_path, "r") as file:
                objdict = json.loads(file.read())
                for o in objdict.values():
                    class_name = o['__class__']
                    del o["__class__"]
                    self.new(eval(class_name)(**o))
        except FileNotFoundError:
            return
