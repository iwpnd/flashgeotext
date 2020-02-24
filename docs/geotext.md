# flashgeotext.geotext

## GeoText
```python
GeoText(self, use_demo_data: bool = True) -> None
```
Extract LookupData from input text

GeoText inherits from LookupDataPool. It iterates through
a LookupDataPool and interfaces flashtext.KeywordProcessor
to extract keywords from an input text. It parses the result of
flashtext.KeywordProcessor.extract_keywords() by counting the
occurances of a LookupData point and optionally lists the
span info.

Example:

    from flashgeotext.geotext import GeoText

    geotext = GeoText(use_demo_data=True)

    input_text = '''Shanghai. The Chinese Ministry of Finance in Shanghai said that China plans
                    to cut tariffs on $75 billion worth of goods that the country
                    imports from the US. Washington welcomes the decision.'''

    geotext.extract(input_text=input_text, span_info=True)
    >> {
        'cities': {
            'Shanghai': {
                'count': 2,
                'span_info': [(0, 8), (45, 53)]
                },
            'Washington, D.C.': {
                'count': 1,
                'span_info': [(175, 185)]
                }
            },
        'countries': {
            'China': {
                'count': 1,
                'span_info': [(64, 69)]
                },
            'United States': {
                'count': 1,
                'span_info': [(171, 173)]
                }
            }
        }

### extract
```python
GeoText.extract(self, input_text: str, span_info: bool = True) -> dict
```
Extract LookupData from an input_text

Arguments:
    input_text (str): String to extract LookupData from.
    span_info (bool): Optionally, return span_info. Defaults to True.

Returns:
    extract_ouput (dict): dictionary of extracted LookupData entities with count
                          and optionally with listed span info.
