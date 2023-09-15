
from utils import apiCallObject
from utils import isDir, isFile, extract_dir_name, extract_file_name
from utils import has_json_in_it
from utils import get_htm_file_path_recursive 


import os

class jsonCreator():

    def __init__(self,path) -> None:
        if not isDir(path):
            raise ValueError(f"The path {path} is not a directory.")    
        self.path = path
        pass

    def setPath(self,newPath):
        if not isDir(newPath):
            raise ValueError(f"The path {newPath} is not a directory.")
        self.path = newPath
        pass

    def getPath(self):
        return self.path
    
    def createJson(self):
        #set up the repo
        repertoire_source = self.path
        if not isDir(repertoire_source):
            raise ValueError(f"The path {repertoire_source} is not a directory.")

        for element in os.listdir(repertoire_source):
            
            subDir = os.path.join(repertoire_source, element)

            if isDir(path=subDir):
            
                #check if the subDir has a json file
                if not has_json_in_it(subDir):
                    #we need to call the api
                    htm_file = get_htm_file_path_recursive(subDir)
                    json_file = apiCallObject(htm_file) 
                    
                    #write the json file
                    with open(os.path.join(subDir,element+".json"),'w') as file:
                        file.write(json_file)
                        file.close()
                            

        
        