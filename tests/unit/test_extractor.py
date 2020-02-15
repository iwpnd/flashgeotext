from flashgeotext.extractor import DemoData
from flashgeotext.extractor import Extractor


def test_extractor_import():
    ext = Extractor()
    assert ext
    assert hasattr(ext, "cities")
    assert hasattr(ext, "countries")


def test_demodata_content():
    demodata = DemoData()

    assert hasattr(demodata, "cities")
    assert hasattr(demodata, "countries")
