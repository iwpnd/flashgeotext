from flashtext import KeywordProcessor
from pydantic import BaseModel


class LookupData(BaseModel):
    name: str
    data: dict


class LookupDataProcessor:
    """
    """

    def __init__(self) -> None:
        self.pool: dict = {}

    def add(self, lookup: LookupData):
        self.pool[lookup.name] = KeywordProcessor(case_sensitive=True)
        self.pool[lookup.name].add_keywords_from_dict(lookup.data)
