import json

from flashtext import KeywordProcessor

from flashgeotext.settings import DEMODATA_CITIES
from flashgeotext.settings import DEMODATA_COUNTRIES


class Alphabets(object):
    pass


class Extractor(object):
    cities_processor: KeywordProcessor = KeywordProcessor(case_sensitive=True)
    countries_processor: KeywordProcessor = KeywordProcessor(case_sensitive=True)


class GeoLookup(Extractor):
    cities: dict = {}
    countries: dict = {}

    def __init__(self, use_demo_data: bool = True):
        self._flush_processor()

        if use_demo_data:
            self.cities = load_data_from_file(file=DEMODATA_CITIES)
            self.countries = load_data_from_file(file=DEMODATA_COUNTRIES)
            self.build_cities_processor()
            self.build_countries_processor()

    def build(self):
        self._flush_processor()
        self.build_cities_processor()
        self.build_countries_processor()

    def build_cities_processor(self):
        if self.cities:
            self.cities_processor.add_keywords_from_dict(self.cities)

    def build_countries_processor(self):
        if self.countries:
            self.countries_processor.add_keywords_from_dict(self.countries)

    def _flush_processor(self):
        self.cities_processor.keyword_trie_dict = dict()
        self.cities_processor._terms_in_trie = 0
        self.countries_processor.keyword_trie_dict = dict()
        self.countries_processor._terms_in_trie = 0


def load_data_from_file(file: str) -> dict:
    with open(file, "r", encoding="utf-8") as f:
        return json.loads(f.read())
