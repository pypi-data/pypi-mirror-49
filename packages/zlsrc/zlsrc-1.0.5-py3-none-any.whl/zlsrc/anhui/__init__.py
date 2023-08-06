import os
from pprint import pprint
dir=os.path.dirname(__file__)
file_list=os.listdir(dir)
file_list.remove('__init__.py')


pprint(file_list)