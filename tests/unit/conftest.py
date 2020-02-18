import pytest

from flashgeotext.geotext import GeoText


@pytest.fixture
def test_data_cities():
    return {"Berlin": ["Berlin", "Dickes B"], "Hamburg": ["Hamburg", "Dickes H"]}


@pytest.fixture
def test_data_countries():
    return {
        "Germany": ["Germany", "Deutschland"],
        "Netherlands": ["The Netherlands", "Netherlands", "Holland"],
    }


@pytest.fixture
def geotext():
    return GeoText(use_demo_data=True)
