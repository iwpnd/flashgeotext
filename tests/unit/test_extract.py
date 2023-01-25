from flashgeotext.geotext import Extract


def test_extract():
    extract = Extract()

    extract.increment_count("test")

    assert len(extract.data.keys()) == 0

    extract.add_span("test", (1, 1))
    assert len(extract.data.keys()) == 0

    extract.add_found_as("test", "test")
    assert len(extract.data.keys()) == 0
