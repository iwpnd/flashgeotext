import pytest
from pydantic import ValidationError

from flashgeotext.lookup import LookupData


def test_lookup_data(test_data_cities):
    lookup = LookupData(name="cities", data=test_data_cities)

    assert lookup.name == "cities"
    assert isinstance(lookup.data, dict)


def test_lookup_data_fails():
    test_data = ["Berlin", "Hamburg"]

    with pytest.raises(ValidationError):
        lookup = LookupData(name="cities", data=test_data)

        assert lookup.name == "cities"
        assert isinstance(lookup.data, dict)
