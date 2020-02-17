import json

from flashtext import KeywordProcessor

from flashgeotext.settings import DEMODATA_CITIES
from flashgeotext.settings import DEMODATA_COUNTRIES


class Alphabets(object):
    pass


class Extractor(object):
    _cities_processor: KeywordProcessor = KeywordProcessor(case_sensitive=True)
    _countries_processor: KeywordProcessor = KeywordProcessor(case_sensitive=True)

    def extract(self, input_text: str, span_info: bool = True):
        return (
            self._cities_processor.extract_keywords(input_text, span_info=span_info),
            self._countries_processor.extract_keywords(input_text, span_info=span_info),
        )


class GeoText(Extractor):
    cities: dict = {}
    countries: dict = {}

    def __init__(self, use_demo_data: bool = True):
        self._flush_processor()

        if use_demo_data:
            self.cities = load_data_from_file(file=DEMODATA_CITIES)
            self.countries = load_data_from_file(file=DEMODATA_COUNTRIES)
            self.build_cities_processor()
            self.build_countries_processor()

    def build(self) -> None:
        self._flush_processor()
        self.build_cities_processor()
        self.build_countries_processor()

    def build_cities_processor(self) -> None:
        if self.cities:
            self._cities_processor.add_keywords_from_dict(self.cities)

    def build_countries_processor(self) -> None:
        if self.countries:
            self._countries_processor.add_keywords_from_dict(self.countries)

    def _flush_processor(self) -> None:
        self._cities_processor.keyword_trie_dict = dict()
        self._cities_processor._terms_in_trie = 0
        self._countries_processor.keyword_trie_dict = dict()
        self._countries_processor._terms_in_trie = 0


def load_data_from_file(file: str) -> dict:
    with open(file, "r", encoding="utf-8") as f:
        return json.loads(f.read())
