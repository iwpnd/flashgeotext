import pytest


text = "Berlin ist die Hauptstadt von Deutschland. Berlin ist nicht haesslich, aber auch nicht sonderlich schoen."


def test_geotext_extract(geotext):
    output = geotext.extract(text)
    assert "Berlin" in output["cities"]


def test_geotext_extract_with_count_span_info_true(geotext):
    output = geotext.extract(input_text=text, span_info=True)
    assert output["cities"]["Berlin"]["count"] == 2
    assert output["cities"]["Berlin"]["span_info"] == [(0, 6), (43, 49)]


def test_geotext_extract_with_count_span_info_false(geotext):
    output = geotext.extract(input_text=text, span_info=False)

    with pytest.raises(KeyError):
        assert output["cities"]["Berlin"]["span_info"] == [(0, 6), (43, 49)]
