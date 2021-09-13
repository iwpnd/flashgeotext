# Table of Contents

* [flashgeotext.geotext](#flashgeotext.geotext)
  * [GeoTextConfiguration](#flashgeotext.geotext.GeoTextConfiguration)
  * [GeoText](#flashgeotext.geotext.GeoText)
    * [\_\_init\_\_](#flashgeotext.geotext.GeoText.__init__)
    * [extract](#flashgeotext.geotext.GeoText.extract)

<a id="flashgeotext.geotext"></a>

# flashgeotext.geotext

<a id="flashgeotext.geotext.GeoTextConfiguration"></a>

## GeoTextConfiguration

```python
class GeoTextConfiguration(BaseModel)
```

GeoText configuration

**Arguments**:

- `use_demo_data` _bool_ - load demo data or not, default True
- `case_sensitive` _bool_ - case sensitive lookup, default True

<a id="flashgeotext.geotext.GeoText"></a>

## GeoText

```python
class GeoText(LookupDataPool)
```

Extract LookupData from input text

GeoText inherits from LookupDataPool. It iterates through
a LookupDataPool and interfaces flashtext.KeywordProcessor
to extract keywords from an input text. It parses the result of
flashtext.KeywordProcessor.extract_keywords() by counting the
occurances of a LookupData point and optionally lists the
span info.

**Example**:

```python
    from flashgeotext.geotext import GeoText

    geotext = GeoText()

    input_text = '''Shanghai. The Chinese Ministry of Finance in Shanghai said that China plans
                    to cut tariffs on $75 billion worth of goods that the country
                    imports from the US. Washington welcomes the decision.'''

    geotext.extract(input_text=input_text, span_info=True)
    >> {
        'cities': {
            'Shanghai': {
                'count': 2,
                'span_info': [(0, 8), (45, 53)],
                'found_as': ['Shanghai', 'Shanghai'],
                },
            'Washington, D.C.': {
                'count': 1,
                'span_info': [(175, 185)],
                'found_as': ['Washington'],
                }
            },
        'countries': {
            'China': {
                'count': 1,
                'span_info': [(64, 69)],
                'found_as': ['China'],
                },
            'United States': {
                'count': 1,
                'span_info': [(171, 173)],
                'found_as': ['US'],
                }
            }
        }

```

<a id="flashgeotext.geotext.GeoText.__init__"></a>

#### \_\_init\_\_

```python
def __init__(config: GeoTextConfiguration = GeoTextConfiguration().dict()) -> None
```

instantiate an empty LookupDataPool, optionally/by default with demo data

**Arguments**:

- `config` - GeoTextConfiguration = { use_demo_data: True, case_sensitive: True }.

<a id="flashgeotext.geotext.GeoText.extract"></a>

#### extract

```python
def extract(input_text: str, span_info: bool = True) -> dict
```

Extract LookupData from an input_text

**Arguments**:

- `input_text` _str_ - String to extract LookupData from.
- `span_info` _bool_ - Optionally, return span_info. Defaults to True.


**Returns**:

- `extract_ouput` _dict_ - dictionary of extracted LookupData entities with count
  and optionally with listed span info.
