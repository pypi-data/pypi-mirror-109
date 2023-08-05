"""
Created on Jun 20, 2014

@author: sstober
"""

import importlib


def load_class(full_class_string):
    """
    dynamically load a class from a string
    """

    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)

    # Finally, we retrieve the Class
    class_ = getattr(module, class_str)
    instance = class_()
    return instance
