#!/usr/bin/python3
"""
The Base module
"""
from uuid import uuid4
from datetime import datetime
import models

class BaseModel:
    """This is the base model of our AirBnb project"""

    def __init__(self, *args, **kwargs):
        """Initialize public instance attributes"""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if len(kwargs) != 0:
            """change format for updated_at & created_at
            """
            for i, j in kwargs.items():
                if i == "created_at" or i == "updated_at":
                    kwargs[i] = datetime.strptime(j, "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    kwargs[i] = j
        else:
            models.storage.new(self)

    def save(self):
        """
            to update time of the model
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
            return the dictionary represenation of an instance
        """
        return {
        **self.__dict__,
        "created_at": self.created_at.isoformat(),
        "updated_at": self.updated_at.isoformat(),
        "__class__": self.__class__.__name__
        }
    
    def __str__(self):
        """
            Then return string representation of the Model
        """
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)

