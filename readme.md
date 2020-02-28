<p align="center">
<a href="https://github.com/iwpnd/flashgeotext/actions" target="_blank">
    <img src="https://github.com/iwpnd/flashgeotext/workflows/build/badge.svg?branch=master" alt="Build Status">
</a>
<a href="https://codecov.io/gh/iwpnd/flashgeotext" target="_blank">
    <img src="https://codecov.io/gh/iwpnd/flashgeotext/branch/master/graph/badge.svg" alt="Coverage">
</a>
</p>

---
# flashgeotext :zap::earth_africa:

Extract and count countries and cities (+their synonyms) from text, like [GeoText](https://github.com/elyase/geotext) on steroids using [FlashText](https://github.com/vi3k6i5/flashtext/), a Aho-Corasick implementation. Flashgeotext is a fast, batteries-included (and BYOD) and native python library that extracts one or more sets of given city and country names (+ synonyms) from an input text.

**documentation**: [https://flashgeotext.iwpnd.pw/](https://flashgeotext.iwpnd.pw/)  
**introductory blogpost**: [https://iwpnd.pw/articles/2020-02/flashgeotext-library](https://iwpnd.pw/articles/2020-02/flashgeotext-library)

## Usage

```python
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
```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

for usage:
```bash
pip install flashgeotext
```

for development:
```bash
git clone https://github.com/iwpnd/flashgeotext.git
pip install flit
flit install
```

### Running the tests

```bash
pytest flashgeotext/tests -v
```

## Authors

* **Benjamin Ramser** - *Initial work* - [iwpnd](https://github.com/iwpnd)

See also the list of [contributors](https://github.com/iwpnd/flashgeotext/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

Demo Data cities from [http://www.geonames.org](http://www.geonames.org) licensed under the Creative Commons Attribution 3.0 License.

## Acknowledgments

* Hat tip to [@vi3k6i5](https://github.com/vi3k6i5) for his [paper](https://arxiv.org/abs/1711.00046) and implementation
