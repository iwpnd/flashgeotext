import json

from flashtext import KeywordProcessor

from flashgeotext.settings import DEMODATA_CITIES
from flashgeotext.settings import DEMODATA_COUNTRIES


class Alphabets(object):
    pass


class LookupData(object):
    cities: dict = {}
    countries: dict = {}

    def __init__(self, use_demo_data: bool = True):
        if use_demo_data:
            self.cities = self._load_data_from_file(file=DEMODATA_CITIES)
            self.countries = self._load_data_from_file(file=DEMODATA_COUNTRIES)

    def _load_data_from_file(self, file: str) -> dict:
        with open(file, "r", encoding="utf-8") as f:
            return json.loads(f.read())


class Extractor(object):
    cities_processor: KeywordProcessor = KeywordProcessor(case_sensitive=True)
    countries_processor: KeywordProcessor = KeywordProcessor(case_sensitive=True)

    def __init__(self):
        self.build_cities_processor()
        self.build_countries_processor()

    def build_cities_processor(self):
        raise NotImplementedError

    def build_countries_processor(self):
        raise NotImplementedError
