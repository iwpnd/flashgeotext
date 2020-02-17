import json

from flashtext import KeywordProcessor

from flashgeotext.settings import DEMODATA_CITIES
from flashgeotext.settings import DEMODATA_COUNTRIES


class Alphabets(object):
    pass


class DemoData(object):
    cities: dict = {}
    countries: dict = {}

    def load(self) -> None:

        self.cities = self._load_data_dict(file=DEMODATA_CITIES)
        self.countries = self._load_data_dict(file=DEMODATA_COUNTRIES)

    def _load_data_dict(self, file: str) -> dict:
        with open(file, "r", encoding="utf-8") as f:
            return json.loads(f.read())


class Extractor:
    cities: KeywordProcessor = KeywordProcessor(case_sensitive=True)
    countries: KeywordProcessor = KeywordProcessor(case_sensitive=True)

    def __init__(self, demo_data: bool = False):

        if demo_data:
            demodata = DemoData()
            self.cities.add_keywords_from_dict(keyword_dict=demodata.cities)
            self.countries.add_keywords_from_dict(keyword_dict=demodata.countries)
