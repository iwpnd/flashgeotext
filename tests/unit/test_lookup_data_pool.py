import pytest

from flashgeotext.lookup import load_data_from_file
from flashgeotext.lookup import LookupData
from flashgeotext.lookup import LookupDataPool
from flashgeotext.lookup import LookupDuplicateError
from flashgeotext.settings import DEMODATA_CITIES
from flashgeotext.settings import SCRIPTS


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


def test_lookup_data_pool_remove_all_from_pool(test_data_cities):
    lookup = LookupData(name="cities", data=test_data_cities)

    processor = LookupDataPool()
    processor.add(lookup)

    processor.remove_all()

    assert not processor.pool


def test_lookup_data_pool_script_non_word_boundaries(test_data_cities):
    lookup = LookupData(name="cities", data=test_data_cities, script="latin")

    processor = LookupDataPool()
    processor.add(lookup)

    assert all(
        [
            char in processor.pool["cities"].non_word_boundaries
            for char in SCRIPTS["latin"]["chars"]
        ]
    )


def test_load_data_from_file():
    cities = load_data_from_file(DEMODATA_CITIES)
    assert cities


def test_load_data_from_file_raises():
    with pytest.raises(TypeError):
        cities = load_data_from_file("demodata_cities.txt")
        assert cities
