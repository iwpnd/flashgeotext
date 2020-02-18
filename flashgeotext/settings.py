import os

PARENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DEMODATA_DIR = os.path.join(PARENT_DIRECTORY, "resources")
DEMODATA_CITIES = DEMODATA_DIR + "/cities.json"
DEMODATA_COUNTRIES = DEMODATA_DIR + "/countries.json"
