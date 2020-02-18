import pytest
from pydantic import ValidationError

from flashgeotext.geotext import GeoText
from flashgeotext.lookup import LookupData
from flashgeotext.lookup import LookupDataPool
from flashgeotext.lookup import LookupDuplicateError


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


def test_lookup_data_pool(test_data_cities):
    lookup = LookupData(name="cities", data=test_data_cities)

    processor = LookupDataPool()
    processor.add(lookup)

    assert processor.pool[lookup.name]


def test_lookup_data_pool_duplicate_data(test_data_cities):
    lookup = LookupData(name="cities", data=test_data_cities)

    processor = LookupDataPool()
    processor.add(lookup)

    with pytest.raises(LookupDuplicateError):
        processor.add(lookup)


def test_lookup_data_pool_add_invalid_lookup(test_data_cities):
    lookup = {"test": ["test", "test2"]}

    processor = LookupDataPool()

    with pytest.raises(TypeError):
        processor.add(lookup)


def test_lookup_data_pool_duplicate_data_update_true(test_data_cities):
    lookup = LookupData(name="cities", data=test_data_cities)

    processor = LookupDataPool()
    processor.add(lookup=lookup, update=True)
    processor.add(lookup=lookup, update=True)

    assert processor.pool["cities"]


def test_lookup_data_pool_remove_lookup_from_pool(test_data_cities):
    lookup = LookupData(name="cities", data=test_data_cities)

    processor = LookupDataPool()
    processor.add(lookup)

    processor.remove(lookup_to_remove="cities")

    with pytest.raises(KeyError):
        assert processor.pool["cities"]


def test_lookup_data_pool_with_test_data():
    geotext = GeoText(use_demo_data=True)

    assert geotext.pool["cities"]
    assert geotext.pool["countries"]
