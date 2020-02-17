import pytest

from flashgeotext.extractor import Extractor
from flashgeotext.extractor import GeoLookup


def test_extractor_import():
    with pytest.raises(NotImplementedError):
        ext = Extractor()
        assert ext


def test_lookupdata_content():
    lookupdata = GeoLookup()

    assert hasattr(lookupdata, "cities")
    assert hasattr(lookupdata, "countries")


def test_lookupdata_load_data():
    lookupdata = GeoLookup()

    assert lookupdata.cities
    assert lookupdata.countries
