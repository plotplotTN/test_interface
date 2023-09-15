from utils.repoOrganiser import repoOrganiser
from utils.jsonCreator import jsonCreator

if __name__ == "__main__":


    #1st step: organise the repo
    repo = r"C:\\Users\\romai\\Downloads\\bordereauxcsv-20230911T144458Z-001\\bordereauxcsv"
    repoOrg = repoOrganiser(repo)
    repoOrg.organise()

    #2nd step: generate the json file corresponding to the bordereau
    jsonCreatorObject = jsonCreator(repo)
    jsonCreatorObject.createJson()

    pass