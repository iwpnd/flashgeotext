import pytest

from flashgeotext.extractor import GeoText


@pytest.fixture
def geotext_demodata():
    geotext_demodata = GeoText()

    return geotext_demodata
