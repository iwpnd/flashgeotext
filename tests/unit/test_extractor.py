from flashgeotext.extractor import Extractor
from flashgeotext.extractor import LookupData


def test_extractor_import():
    ext = Extractor()
    assert ext
    assert hasattr(ext, "cities")
    assert hasattr(ext, "countries")


def test_lookupdata_content():
    lookupdata = LookupData()

    assert hasattr(lookupdata, "cities")
    assert hasattr(lookupdata, "countries")


def test_lookupdata_load_data():
    lookupdata = LookupData(use_demo_data=True)

    assert lookupdata.cities
    assert lookupdata.countries
