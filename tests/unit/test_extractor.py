import pytest

from flashgeotext.extractor import Extractor
from flashgeotext.extractor import GeoLookup


def test_extractor_init():
    ext = Extractor()

    assert hasattr(ext, "cities_processor")
    assert hasattr(ext, "countries_processor")


def test_geolookup_demo_data():
    geolookup_with_demodata = GeoLookup(use_demo_data=True)

    assert geolookup_with_demodata.cities
    assert geolookup_with_demodata.cities_processor
    assert geolookup_with_demodata.countries
    assert geolookup_with_demodata.countries_processor


def test_geolookup_no_demo_data_and_empty_processor():
    geolookup_empty = GeoLookup(use_demo_data=False)

    assert not geolookup_empty.cities
    assert not geolookup_empty.countries
    assert len(geolookup_empty.countries_processor) == 0
    assert len(geolookup_empty.cities_processor) == 0


@pytest.mark.parametrize(
    "cities, countries, len_countries_processor, len_cities_processor",
    [
        (
            {
                "Berlin": ["Berlin", "german capitol"],
                "Kopenhagen": ["Kopenhagen", "danish capitol"],
            },
            {"Germany": ["Germany"], "Denmark": ["Denmark"]},
            2,
            4,
        )
    ],
)
def test_geolookup_manual_data(
    cities, countries, len_countries_processor, len_cities_processor
):
    geolookup = GeoLookup()
    geolookup.cities = cities
    geolookup.countries = countries

    geolookup.build()

    assert len(geolookup.cities_processor) == len_cities_processor
    assert len(geolookup.countries_processor) == len_countries_processor
