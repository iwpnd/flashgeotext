import json

from flashtext import KeywordProcessor
from loguru import logger
from pydantic import BaseModel
from pydantic import StrictStr

from flashgeotext.settings import DEMODATA_CITIES
from flashgeotext.settings import DEMODATA_COUNTRIES


class LookupDuplicateError(Exception):
    """Exception is raised if LookupData is already in LookupDataPool

    Args:
        message (str): Human readable string describing the exception.

    Attributes:
        message (str): Human readable string describing the exception.
    """

    def __init__(self, message: str):
        self.message = message


class MissingLookupDataError(Exception):
    """Exception is raised if GeoText.extract() is used on empty LookupDataPool

    Args:
        message (str): Human readable string describing the exception.

    Attributes:
        message (str): Human readable string describing the exception.
    """

    def __init__(self, message: str):
        self.message = message


class LookupValidation:
    """Data validation container object

    Args:
        status (str): Humanreadible string containing the Error status.
        error_count (int): Error count in validation data.
        errors (dict):

        Example: {
            "Berlin": [
                "Berlin missing in list of synonyms",
                "data['Berlin'] is not a list of synonyms"
                ]
            }

    Arguments:
        status (str): Humanreadible string containing the Error status.
        error_count (int): Error count in validation data.
        errors (dict):

        Example: {
            "Berlin": [
                "Berlin missing in list of synonyms",
                "data['Berlin'] is not a list of synonyms"
                ]
            }
    """

    def __init__(
        self,
        status: str = "No errors detected",
        error_count: int = 0,
        errors: dict = {},
    ):
        self.status = status
        self.error_count = error_count
        self.errors = {}


class LookupData(BaseModel):
    """Data that is supposed to be looked up in a text

    Args:
        name (pydantic.StrictStr): Human readable name as string describing the data.
        data (dict): dictionary containing data to lookup and their synonyms

    Attributes:
        name (pydantic.StrictStr): Human readable name as string describing the data.
        data (dict): dictionary containing data to lookup and their synonyms
    """

    name: StrictStr
    data: dict

    def validate(self) -> dict:
        """Validate if data attribute has appropiate structure.

        returns:
            LookupValidation
        """

        validation = LookupValidation()

        for key, value in self.data.items():
            if not isinstance(value, list):
                validation.errors[key] = [f"data[{key}] is not a list of synonyms"]
                validation.error_count = validation.error_count + 1

            if key not in value:
                if key in validation.errors:
                    validation.errors[key] = validation.errors[key] + [
                        f"{key} missing in list of synonyms"
                    ]
                else:
                    validation.errors[key] = [f"{key} missing in list of synonyms"]

                validation.error_count = validation.error_count + 1

        if validation.error_count > 0:
            validation.status = f"Found {validation.error_count} errors"

        return validation


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
