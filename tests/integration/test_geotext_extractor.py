import pytest

from flashgeotext.geotext import GeoText
from flashgeotext.lookup import LookupData
from flashgeotext.lookup import MissingLookupDataError

text = "Berlin ist die Hauptstadt von Deutschland. Berlin ist nicht haesslich, aber auch nicht sonderlich schoen."


def test_geotext_demo_data():
    geotext = GeoText(use_demo_data=True)

    assert geotext.pool["cities"]
    assert geotext.pool["countries"]


def test_geotext_extract(geotext):
    output = geotext.extract(text)
    assert "Berlin" in output["cities"]


def test_geotext_raises_on_empty_pool():
    output = GeoText(use_demo_data=False)

    with pytest.raises(MissingLookupDataError):
        output.extract(text)


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
        pytest.param(
            6,
            """A high-speed passenger train derailed in the early hours of Thursday morning near Milan, northern Italy.
            Officials said that the train was traveling at 180 mph when the engine car derailed,
            separated from the train, and slammed into a railroad building. The train was travelling to
            Bologna, with 33 people on board. Two railway workers were killed, and 27 people were injured.""",
            ["Milano", "Bologna"],
            id="english1-synonym",
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
            id="english1-synonym",
        ),
        pytest.param(
            2,
            """The Chinese Ministry of Finance said that China plans
            to cut tariffs on $75 billion worth of goods that the country
            imports from the US.""",
            ["China", "United States"],
            id="english2-synonym",
        ),
        pytest.param(
            2,
            """Israel wants to take a part of Palestine’s area. Palestine is not happy about it.
            It is not good for the power of Palestine. People in Palestine are angry.
            Palestine is inside Israel if Israel takes the area.
            The US makes a new plan for peace for Israel and Palestine.
            The US agrees with Israel. The US supports Israel´s plan to take a part of Palestine.""",
            ["Palestine", "United States", "Israel"],
            id="english3-synonym",
        ),
    ],
)
def test_geotext_extract_countries(nr, text, expected_countries, geotext):
    output = geotext.extract(input_text=text, span_info=False)

    assert all([country in output["countries"] for country in expected_countries])


def test_geotext_with_script_added_to_non_word_boundaries():
    cyrillic = LookupData(
        name="test_1", data={"Нижневартовск": ["Нижневартовск"]}, script="cyrillic"
    )
    geotext = GeoText(use_demo_data=False)
    geotext.add(cyrillic)

    text = """
    В Нижневартовском районе ограничили грузоподъемность на ледовых переправах
    Проехать по ледовой переправе сможет только транспорт весом не более 5 тонн.
    В связи с потеплением в Нижневартовском районе введено ограничение грузоподъемности на ледовых переправах.
    По направлению Нижневартовск - Вампугол – Былино, а также Белорусский - Ларьяк , Ларьяк -
    Чехломей - Большой Ларьяк, Былино - Зайцева Речка снижена грузоподъемность до 5 тонн.
    Лед на реках еще вполне толстый и переправа пригодна для эксплуатации, однако зимник начал подтаивать,
    орогу развезло. Потому принято решение снизить грузоподъемность на нём до 5 тонн, сообщает ОТРК «Югра».
    Всего на реках Югры работают 89 ледовых переправ. Их обычная грузоподъемность от 15 до 30 тонн. Отметим,
    что традиционно в середине апреля закрываются для движения автотранспорта все ледовые переправы.
    """

    result = geotext.extract(text, span_info=False)
    result["test_1"]["Нижневартовск"]["count"] == 1
