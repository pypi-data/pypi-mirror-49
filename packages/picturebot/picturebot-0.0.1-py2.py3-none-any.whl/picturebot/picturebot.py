import json
import generalutils.guard as grd
import os
from dataclasses import dataclass
import argparse

@dataclass
class Config:
    '''POCO class for config data'''

    Workplace: str = ""
    Workflow: str = ""
    Baseflow: str = ""

def FullFilePath(*items):
    '''Get the full path to a folder or directory
    Args:
        items (list): List of folders and subfolders
    
    Returns:
        (string) Full file name
    '''

    # Get the current working directory
    path = os.path.dirname(os.path.abspath(__file__))

    # Loop over every folder and subfolders
    for item in items:
        path = os.path.join(path, item)

    return path

def CreateFolder(path):
    '''Create And test whether the folder is successfully created
    
    Args:
        path (string): Folder that is going to get created
    '''

    if not grd.Filesystem.IsPath(path):
        # Create folder
        os.mkdir(path)

        # Check whether creation was successfull
        grd.Filesystem.PathExist(path)


pa = argparse.ArgumentParser()
pa.add_argument('-c', '--create', help="Create workflow directories", action='store_true')
pa.add_argument('-r','--rename', help="Rename the files within the baseflow directory", action='store_true')

args = pa.parse_args()

# Obtain the full path to the config file
pathToConfig = FullFilePath("config","config.json")
# Check whether the path to the confile exists
grd.Filesystem.PathExist(pathToConfig)

with open(pathToConfig) as f:
    # Load data from file
    data = json.load(f)
    config = Config(data['workplace'], data['workflow'], data['baseflow'])

# Create new workspace
if grd.Argument.IsValid(args.create):
    #Check whether the workplace folder exists    
    grd.Filesystem.PathExist(config.Workplace)

    #Loop-over the workflows
    for flow in config.Workflow:
        pathToFlow = FullFilePath(config.Workplace,flow)
        CreateFolder(pathToFlow)
        grd.Filesystem.PathExist(pathToFlow)

# Rename pictures within workflow directory
elif grd.Argument.IsValid(args.rename):
    # Get the current working directory of where the script is executed
    cwd = os.getcwd()

    # Check whether the current working directory exists
    grd.Filesystem.PathExist(cwd)

    # Obtain the name of the base directory of the current working directory
    basename = os.path.basename(cwd)

    # Loop-ver the workflows and add an project directory to each flow
    for flow in config.Workflow:
        # Obtain the path to the project flow
        pathToFlowProject = FullFilePath(config.Workplace,flow,basename)

        CreateFolder(pathToFlowProject)

        grd.Filesystem.PathExist(pathToFlowProject)

        print(f"Added folder: {pathToFlowProject}")

    print('\r\n')

    flow = ''
    counter = 0

    # Loop over every word of the flow name directory
    for i in basename.split(' '):
        # Append the individual words to an '_'
        flow += f'{i}_'

    # Obtain the original picture name within a flow directory
    pictures = os.listdir(cwd)
    # sort by date
    pictures.sort(key=os.path.getmtime)

    # Loop over every picture withing the flow directory
    for index, picture in enumerate(pictures, 1):
        # Get the extension of the original picture
        extension = picture.split('.')[1]

        # Get absolute path to the picture
        pathToPicture = os.path.join(cwd,picture)

        # Check whether the absolute path to the picture is existing
        grd.Filesystem.PathExist(pathToPicture)

        # Get the new name for the picture
        newName = f"{flow}{index}.{extension}"

        # Obtain the absolute path to the new picture name
        pathToNewPicture = os.path.join(cwd, newName)

        # Rename the picture file
        os.rename(pathToPicture, pathToNewPicture)

        print(f"Renaming: {picture} -> {newName}")

        # Check whether the new picture file exists after renaming
        grd.Filesystem.PathExist(pathToNewPicture)

        counter += 1
    
    print(f"Renamed files: {counter}")