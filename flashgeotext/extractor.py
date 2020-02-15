import json
from typing import Union

from flashtext import KeywordProcessor

from flashgeotext.settings import DEMODATA_CITIES
from flashgeotext.settings import DEMODATA_COUNTRIES


class Alphabets(object):
    pass


class DemoData(object):
    cities: Union[list, dict] = []
    countries: Union[list, dict] = []

    def __init__(self, with_synonyms: bool = True):
        self.load_demo_data(with_synonyms=with_synonyms)

    def load_demo_data(self, with_synonyms: bool = True) -> None:

        if with_synonyms:
            self.cities = self._load_data_dict(file=DEMODATA_CITIES)
            self.countries = self._load_data_dict(file=DEMODATA_COUNTRIES)

        else:
            self.cities = self._load_data_list(file=DEMODATA_CITIES)
            self.countries = self._load_data_list(file=DEMODATA_COUNTRIES)

    def _load_data_dict(self, file: str = "") -> dict:
        with open(file, "r", encoding="utf-8") as f:
            return json.loads(f.read())

    def _load_data_list(self, file: str = "") -> list:
        with open(file, "r", encoding="utf-8") as f:
            return list(json.loads(f.read()).keys())


class Extractor:
    cities: KeywordProcessor = KeywordProcessor(case_sensitive=True)
    countries: KeywordProcessor = KeywordProcessor(case_sensitive=True)

    def __init__(self, demo_data: bool = False):

        if demo_data:
            demodata = DemoData()
            self.cities.add_keywords_from_dict(keyword_dict=demodata.cities)
            self.countries.add_keywords_from_dict(keyword_dict=demodata.countries)
