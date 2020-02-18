from flashtext import KeywordProcessor
from loguru import logger
from pydantic import BaseModel


class LookupDuplicateError(Exception):
    pass


class LookupData(BaseModel):
    name: str
    data: dict


class LookupDataProcessor:
    """
    """

    def __init__(self) -> None:
        self.pool: dict = {}

    def add(self, lookup: LookupData, update: bool = False) -> None:
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


class GeoText(LookupDataProcessor):
    def __init__(self):
        pass
