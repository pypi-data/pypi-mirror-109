'''

convenience functions to help speed up the work

'''

import os
from copy import deepcopy
import inspect


# find path of the file doing the importing
for frame in inspect.stack()[1:]:
    if frame.filename[0] != '<':
        importing_dir = frame.filename
        break

class getpath(str):
    '''
    '''
    def __new__(cls, *args, custom=False):
        if custom:
            paths = []
        else:
            paths = [os.path.dirname(importing_dir)]
        
        for arguments in args:
            if arguments == '..':
                paths[0] = os.path.split(paths[0])[0]
            else:
                paths.append(arguments)
        
        path = os.sep.join(paths)
        return str.__new__(cls, path)
    
    def __init(self):
        super().__init__(self)
    
    def add(self, *args):
        paths = []
        for arguments in args:
            paths.append(arguments)
        
        path = os.sep.join([self.__str__(), os.sep.join(paths)])
        return getpath(path, custom=True)
    
    def __truediv__(self, *args):
        current_path = deepcopy(self.__str__())

        paths = [current_path]
        
        for arguments in args:
            if arguments == '..':
                paths[0] = os.path.split(paths[0])[0]
            else:
                paths.append(arguments)
        
        path = os.sep.join(paths)
        return getpath(path, custom=True)
    
    def ls(self, *args):
        paths = []
        for arguments in args:
            paths.append(arguments)
        
        path = os.sep.join([self.__str__(), os.sep.join(paths)])

        files_and_stuff = os.listdir(path)
        
        return files_and_stuff
    
    def up(self, num, *args):
        paths = []
        for arguments in args:
            paths.append(arguments)
        
        path = os.sep.join([self.__str__(), os.sep.join(paths)])

        times_up = ['..' for i in range(num+1)]
        return getpath(path, *times_up, custom=True)