import json
import sys
from typing import Dict, List

from flashtext import KeywordProcessor
from loguru import logger
from pydantic import BaseModel, StrictStr, validator

from flashgeotext import settings

logger.remove()
logger.add(sys.stderr, level=settings.LOGLEVEL)


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


class ValidationResult(BaseModel):
    status: str = "No errors detected"
    error_count: int = 0
    errors: Dict[str, List[str]] = {}


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
    """

    data: ValidationResult

    def __init__(self):
        self.data = ValidationResult()

    def has_error(self, name: str) -> bool:
        return name in self.data.errors

    def get_error_count(self) -> int:
        return self.data.error_count

    def set_error_status(self) -> None:
        self.data.status = f"Found {self.data.error_count} errors"

    def add_error(self, name: str, error: str) -> None:
        if not self.has_error(name):
            self.data.errors[name] = [error]
            self.data.error_count = self.data.error_count + 1
            return

        self.data.errors[name].append(error)
        self.data.error_count = self.data.error_count + 1

    def to_dict(self):
        return self.data.dict()


class LookupData(BaseModel, object):
    """Data that is supposed to be looked up in a text

    Setting a script here would add characters of that script (see resources/scripts.json)
    to the set of non_word_boundaries's default of:
    >> {'k', '6', 's', 'M', 'i', 'S', 'm', 'E', 'r', 'W', 'v', 'l',
        'R', 'f', 'e', 'X', '7', '3', 'q', 'w', '0', 'x', 'V', 'C', 'n',
        'I', '4', 'D', 'z', 'G', 'L', '2', 'T', 'U', '_', 'B', 't', 'Q',
        'd', '9', 'h', 'o', 'c', 'u', 'P', 'K', 'Y', 'p', 'A', 'J', 'O',
        'N', 'H', 'j', 'a', 'Z', '5', '1', 'b', 'y', 'F', '8', 'g'}

    Args:
        name (pydantic.StrictStr): Human readable name as string describing the data.
        data (dict): dictionary containing data to lookup and their synonyms
        script: (pydantic.StrictStr): what scripts characters to add to non_word_boundaries

    Attributes:
        name (pydantic.StrictStr): Human readable name as string describing the data.
        data (dict): dictionary containing data to lookup and their synonyms
        script: (pydantic.StrictStr): what scripts characters to add to non_word_boundaries
    """

    name: StrictStr
    data: dict
    script: StrictStr = "default"

    @validator("script")
    def script_must_be_in_scripts(cls, value):
        if value not in settings.SCRIPTS:
            raise ValueError("must be supported script")
        return value

    def validate(self) -> dict:
        """Validate if data attribute has appropiate structure.

        returns:
            LookupValidation
        """

        validation = LookupValidation()

        for key, value in self.data.items():
            if not isinstance(value, list):
                validation.add_error(key, f"{key} is not a list of synonyms")
                validation.add_error(key, f"{key} missing in list of synonyms")

            if isinstance(value, list) and key not in value:
                validation.add_error(key, f"{key} missing in list of synonyms")

        if validation.get_error_count() > 0:
            validation.set_error_status()

        return validation.to_dict()


class LookupDataPool:
    """Collection of KeywordProcessors from LookupData

    Args:
        pool (dict): Collection of LookupData.

    Attributes:
        pool (dict): Collection of LookupData.

    Example:
        pool = {
            LookupData.name: flashtext.KeywordProcessor.add_keywords_from_dict(LookupData.data)
            }
    """

    def __init__(self) -> None:
        self.pool: dict = {}

    def add(
        self, lookup: LookupData, update: bool = False, case_sensitive: bool = True
    ) -> None:
        """Add LookupData to LookupDataPool

        Add LookupData to LookupDataPool.
        Raises flashgeotext.lookup.LookupDuplicateError if lookup
        is already in pool unless update == True.

        Args:
            lookup (LookupData): LookupData to add to pool
            update (bool): Allow update of an existing entry in LookupDataPool, default False
            case_sensitive (bool): Allow case-sensitive lookup, default True
        """
        if not isinstance(lookup, LookupData):
            raise TypeError("lookup has to be instance of LookupData")

        if lookup.name in self.pool and not update:
            raise LookupDuplicateError(
                f"'{lookup.name}' has already been added. Set update=True to update"
            )
        else:
            self.pool[lookup.name] = KeywordProcessor(case_sensitive=case_sensitive)
            self.pool[lookup.name].add_keywords_from_dict(lookup.data)

            # if there is a script specified, then update non word boundaries with
            # characters from script

            if lookup.script != "default":
                self.pool[lookup.name].non_word_boundaries.update(
                    settings.SCRIPTS[lookup.script]["chars"]
                )

            logger.debug(f"{lookup.name} added to pool")

    def remove(self, lookup_to_remove: str) -> None:
        """Remove LookupData from LookupDataPool

        Args:
            lookup_to_remove (str): LookupData to remove from pool
        """
        if lookup_to_remove in self.pool:
            del self.pool[lookup_to_remove]
            logger.debug(f"{lookup_to_remove} removed from pool")

    def remove_all(self):
        """Remove all LookupData from LookupDataPool"""

        self.pool = {}

    def _add_demo_data(self, case_sensitive: bool = True):
        """(private) Add demo data to pool

        Adds DEMODATA_CITIES and DEMODATA_COUNTRIES to LookupDataPool
        """
        cities = LookupData(
            name="cities", data=load_data_from_file(file=settings.DEMODATA_CITIES)
        )
        countries = LookupData(
            name="countries", data=load_data_from_file(file=settings.DEMODATA_COUNTRIES)
        )
        self.add(cities, case_sensitive=case_sensitive)
        self.add(countries, case_sensitive=case_sensitive)
        logger.debug(f"demo data loaded for: {list(self.pool.keys())}")


def load_data_from_file(file: str) -> dict:
    """Load data from json file

    Load data from json file. Raises TypeError if not json

    Args:
        file (str): path to file
    """

    if not file.endswith(".json"):
        raise TypeError("File has to be Filetype .json")

    with open(file, "r", encoding="utf-8") as f:
        return json.loads(f.read())
