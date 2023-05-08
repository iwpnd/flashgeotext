<p align="center">
<a href="https://github.com/iwpnd/flashgeotext/actions" target="_blank">
    <img src="https://github.com/iwpnd/flashgeotext/workflows/CI/badge.svg?branch=master" alt="Build Status">
</a>
<a href="https://codecov.io/gh/iwpnd/flashgeotext" target="_blank">
    <img src="https://codecov.io/gh/iwpnd/flashgeotext/branch/master/graph/badge.svg" alt="Coverage">
</a>
</p>

---

# flashgeotext :zap::earth_africa:

Extract and count countries and cities (+their synonyms) from text, like [GeoText](https://github.com/elyase/geotext) on steroids using [FlashText](https://github.com/vi3k6i5/flashtext/), a Aho-Corasick implementation. Flashgeotext is a fast, batteries-included (and BYOD) and native python library that extracts one or more sets of given city and country names (+ synonyms) from an input text.

**introductory blogpost**: [https://iwpnd.github.io/articles/2020-02/flashgeotext-library](https://iwpnd.pw/articles/2020-02/flashgeotext-library)

## Usage

```python
from flashgeotext.geotext import GeoText

geotext = GeoText()

input_text = '''Shanghai. The Chinese Ministry of Finance in Shanghai said that China plans
                to cut tariffs on $75 billion worth of goods that the country
                imports from the US. Washington welcomes the decision.'''

geotext.extract(input_text=input_text)
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

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

pip:

```bash
pip install flashgeotext
```

conda:

```bash
conda install flashgeotext
```

for development:

```bash
git clone https://github.com/iwpnd/flashgeotext.git
cd flashgeotext/
poetry install
```

### Running the tests

```bash
poetry run pytest . -v
```

## Authors

- **Benjamin Ramser** - _Initial work_ - [iwpnd](https://github.com/iwpnd)

See also the list of [contributors](https://github.com/iwpnd/flashgeotext/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

Demo Data cities from [http://www.geonames.org](http://www.geonames.org) licensed under the Creative Commons Attribution 3.0 License.

## Acknowledgments

- Hat tip to [@vi3k6i5](https://github.com/vi3k6i5) for his [paper](https://arxiv.org/abs/1711.00046) and implementation
