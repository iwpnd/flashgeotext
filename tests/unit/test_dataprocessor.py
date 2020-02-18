import pytest
from pydantic import ValidationError

from flashgeotext.lookup import LookupData
from flashgeotext.lookup import LookupDataProcessor


def test_lookup_data():
    test_data = {"Berlin": ["Berlin", "Dickes B"], "Hamburg": ["Hamburg", "Dickes H"]}

    lookup = LookupData(name="cities", data=test_data)

    assert lookup.name == "cities"
    assert isinstance(lookup.data, dict)


def test_lookup_data_fails():
    test_data = ["Berlin", "Hamburg"]

    with pytest.raises(ValidationError):
        lookup = LookupData(name="cities", data=test_data)

        assert lookup.name == "cities"
        assert isinstance(lookup.data, dict)


def test_lookup_data_processor():
    test_data = {"Berlin": ["Berlin", "Dickes B"], "Hamburg": ["Hamburg", "Dickes H"]}

    lookup = LookupData(name="cities", data=test_data)

    processor = LookupDataProcessor()
    processor.add(lookup)

    assert processor
