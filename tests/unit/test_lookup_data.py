import pytest
from pydantic import ValidationError

from flashgeotext.lookup import LookupData


def test_lookup_data(test_data_cities):
    lookup = LookupData(name="cities", data=test_data_cities)

    assert lookup.name == "cities"
    assert isinstance(lookup.data, dict)


@pytest.mark.parametrize(
    "id, name, data, expectation",
    [
        (1, "cities", ["Berlin", "Hamburg"], pytest.raises(ValidationError)),
        (2, "cities", ("Berlin", "Hamburg"), pytest.raises(ValidationError)),
        (3, "cities", "Berlin", pytest.raises(ValidationError)),
        (4, "cities", 1337, pytest.raises(ValidationError)),
        (5, 1337, {"Berlin": ["Berlin"]}, pytest.raises(ValidationError)),
        (6, [13, 37], {"Berlin": ["Berlin"]}, pytest.raises(ValidationError)),
        (7, (13, 37), {"Berlin": ["Berlin"]}, pytest.raises(ValidationError)),
        (8, {"13": 37}, {"Berlin": ["Berlin"]}, pytest.raises(ValidationError)),
    ],
)
def test_lookup_data_raises(id, name, data, expectation):

    with expectation:
        lookup = LookupData(name=name, data=data)

        assert isinstance(lookup, LookupData)
