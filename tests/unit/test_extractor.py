import pytest

from flashgeotext.extractor import Extractor
from flashgeotext.extractor import GeoText


def test_extractor_init():
    ext = Extractor()

    assert hasattr(ext, "cities_processor")
    assert hasattr(ext, "countries_processor")


def test_extractor_extract(geotext_demodata):
    geotext = geotext_demodata

    assert geotext.extract("I love Berlin")


def test_geolookup_demo_data(geotext_demodata):
    geotext = geotext_demodata

    assert geotext.cities
    assert geotext.cities_processor
    assert geotext.countries
    assert geotext.countries_processor


def test_geolookup_no_demo_data_and_empty_processor():
    geolookup_empty = GeoText(use_demo_data=False)

    assert not geolookup_empty.cities
    assert not geolookup_empty.countries
    assert len(geolookup_empty.countries_processor) == 0
    assert len(geolookup_empty.cities_processor) == 0


@pytest.mark.parametrize(
    "cities, countries, len_cities_processor, len_countries_processor",
    [
        (
            {
                "Berlin": ["Berlin", "german capitol"],
                "Kopenhagen": ["Kopenhagen", "danish capitol"],
            },
            {"Germany": ["Germany"], "Denmark": ["Denmark"]},
            4,
            2,
        ),
        ({}, {"Germany": ["Germany"], "Denmark": ["Denmark"]}, 0, 2),
        (
            {
                "Berlin": ["Berlin", "german capitol"],
                "Kopenhagen": ["Kopenhagen", "danish capitol"],
            },
            {},
            4,
            0,
        ),
    ],
)
def test_geolookup_manual_data(
    cities, countries, len_cities_processor, len_countries_processor, geotext_demodata
):
    geolookup = geotext_demodata
    geolookup.cities = cities
    geolookup.countries = countries

    geolookup.build()

    assert len(geolookup.cities_processor) == len_cities_processor
    assert len(geolookup.countries_processor) == len_countries_processor
