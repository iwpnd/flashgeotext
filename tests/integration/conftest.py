import pytest

from flashgeotext.geotext import GeoText


@pytest.fixture
def geotext():
    return GeoText(use_demo_data=True)
