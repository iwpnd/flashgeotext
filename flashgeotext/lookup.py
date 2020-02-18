import json

from flashtext import KeywordProcessor
from loguru import logger
from pydantic import BaseModel

from flashgeotext.settings import DEMODATA_CITIES
from flashgeotext.settings import DEMODATA_COUNTRIES


class LookupDuplicateError(Exception):
    pass


class MissingLookupDataError(Exception):
    pass


class LookupData(BaseModel):
    name: str
    data: dict


class LookupDataPool:
    """
    """

    def __init__(self) -> None:
        self.pool: dict = {}

    def add(self, lookup: LookupData, update: bool = False) -> None:
        if not isinstance(lookup, LookupData):
            raise TypeError(f"lookup has to be instance of LookupData")

        if lookup.name in self.pool and not update:
            raise LookupDuplicateError(
                f"'{lookup.name}' has already been added. Set update=True to update"
            )
        else:
            self.pool[lookup.name] = KeywordProcessor(case_sensitive=True)
            self.pool[lookup.name].add_keywords_from_dict(lookup.data)
            logger.debug(f"{lookup.name} added to pool")

    def remove(self, lookup_to_remove: str) -> None:
        if lookup_to_remove in self.pool:
            del self.pool[lookup_to_remove]
            logger.debug(f"{lookup_to_remove} removed from pool")

    def _add_demo_data(self):
        cities = LookupData(
            name="cities", data=load_data_from_file(file=DEMODATA_CITIES)
        )
        countries = LookupData(
            name="countries", data=load_data_from_file(file=DEMODATA_COUNTRIES)
        )
        self.add(cities)
        self.add(countries)
        logger.debug(f"demo data loaded for: {list(self.pool.keys())}")


def load_data_from_file(file: str) -> dict:
    with open(file, "r", encoding="utf-8") as f:
        return json.loads(f.read())
