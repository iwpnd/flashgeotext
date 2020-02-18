from flashgeotext.extractor import Extractor
from flashgeotext.lookup import LookupDataPool


class GeoText(LookupDataPool, Extractor):
    def __init__(self, use_demo_data: bool = True) -> None:
        self.pool: dict = {}

        if use_demo_data:
            self._add_demo_data()
