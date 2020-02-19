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


# tests used in geotext (https://github.com/elyase/geotext)


@pytest.mark.parametrize(
    "nr, text, expected_cities",
    [
        pytest.param(
            1,
            """As capitais do nordeste brasileiro são:
            Salvador na Bahia, Recife em Pernambuco, Natal fica no Rio Grande do Norte, João Pessoa fica na Paraíba,
            Fortaleza fica no Ceará, Teresina no Piauí, Aracaju em Sergipe, Maceió em Alagoas e São Luís no Maranhão.""",
            [
                "Salvador",
                "Recife",
                "Natal",
                "Rio Grande",
                "João Pessoa",
                "Fortaleza",
                "Teresina",
                "Aracaju",
                "Maceió",
                "São Luís",
            ],
            id="northeast brazil",
        ),
        pytest.param(
            2,
            """As capitais dos estados do norte brasileiro são: Manaus no Amazonas,
            Palmas em Tocantins, Belém no Pará, Acre no Rio Branco.""",
            ["Manaus", "Palmas", "Belém", "Rio Branco"],
            id="northern brazil",
        ),
        pytest.param(
            3,
            """São Paulo é a capital do estado de São Paulo. As cidades de Barueri
            e Carapicuíba fazem parte da Grade São Paulo. O Rio de Janeiro continua lindo.
            No carnaval eu vou para Salvador. No reveillon eu quero ir para Santos.""",
            [
                "São Paulo",
                "São Paulo",
                "Barueri",
                "Carapicuíba",
                "Rio de Janeiro",
                "Salvador",
                "Santos",
            ],
            id="southeast brazil",
        ),
        pytest.param(
            4,
            """As capitais da região centro-oeste do Brasil são:
            Goiânia em Goiás, Brasília no Distrito Federal, Campo Grande no Mato Grosso do Sul,
            Cuiabá no Mato Grosso.""",
            ["Goiânia", "Goiás", "Brasília", "Campo Grande", "Cuiabá"],
            id="central brazil",
        ),
        pytest.param(
            5,
            """As capitais da região sul são:
            Porto Alegre no Rio Grande do Sul, Floripa em Santa Catarina,
            Curitiba no Paraná""",
            ["Porto Alegre", "Rio Grande", "Santa Catarina", "Curitiba", "Paraná"],
            id="south brazil",
        ),
    ],
)
def test_geotext_extract_cities(nr, text, expected_cities, geotext):
    output = geotext.extract(input_text=text, span_info=False)

    assert all([city in output["cities"] for city in expected_cities])


@pytest.mark.parametrize(
    "nr, text, expected_countries",
    [
        pytest.param(
            1,
            """The total use of coal to generate electricity is set
            to decrease by 3 percent this year. This amounts to the
            total coal use by Germany, UK, and Spain combined.""",
            ["Germany", "United Kingdom", "Spain"],
            id="english1",
        ),
        pytest.param(
            2,
            """The Chinese Ministry of Finance said that China plans
            to cut tariffs on $75 billion worth of goods that the country
            imports from the US.""",
            ["China", "United States"],
            id="english2",
        ),
    ],
)
def test_geotext_extract_countries(nr, text, expected_countries, geotext):
    output = geotext.extract(input_text=text, span_info=False)

    assert all([country in output["countries"] for country in expected_countries])
