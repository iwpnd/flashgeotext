# flashgeotext :zap::earth_africa:

Extract and count countries and cities (+their synonoms) from text, like [GeoText](https://github.com/elyase/geotext) on steroids using [FlashText](https://github.com/vi3k6i5/flashtext/), a Aho-Corasick implementation.

# Usage

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

# Description

I was approached with the question if I could extract a given set of city names from a text. At first I was like :smirk::+1:, but very quickly I noticed that the task was not as trivial as I thought it would be. :cold_sweat:

1. if you match every word in a lookup with every match in an input_text, you're left with m*n calculations.
2. if the city you're looking for consists of more than one word, you have to match against [n-grams](https://blog.xrds.acm.org/2017/10/introduction-n-grams-need/) of the input text.
3. if you happen to want to find synonyms of your city names you have to come up with a data structure to match the city name to its synonyms and vice versa
4. you're not allowed to use elasticsearch :frowning:

Let's see if there are already solution out there.

## GeoText

[GeoText](https://github.com/elyase/geotext) relies on a single regex search pattern to extract named entities from an input text. Afterwards GeoText tries to match every single one of the entities found to a collection of city and country names one by one. This approach is fast for the 22.000 cities that come with the library, but do not scale well with longer texts and more cities/keywords in a lookup file. GeoText also does not make it easy to bring your own data. Also synonyms are not in the scope of GeoText. Another problem is the regex search pattern that extracts named entities. It is a fine line between matching correctly and matching too much, and it get's even harder to match, when city names contain of more than a couple of words.

```python
from geotext import GeoText

text = "I live in Ixtapan de la Sal."
GeoText(text).cities
>> []
```

## spaCy

[spaCy](https://github.com/explosion/spaCy) is awesome. It supports a lot of languages. It's easy to learn, hard to master. It's super well documented and embedded into a great community and a great ecosystem of plugins/addons/spinoffs. It has a lot of functionality aside from named entity extraction. And it does what it is supposed to do and more. However, named entity extraction with spaCy is still based on a trained models prediction, and even though the core models perform really good, they are not 100% accurate. And to go on, even if you extract all location/cities/countries from an input text, you still have to match if you want a normalized output. There is also no support to count occurances, let alone handle synonyms. On top of that spaCy is build with C dependencies and you are limited to the pre-trained models, unless you want to train your own language model from scratch.

## FlashText

> FlashText can search or replace keywords in one pass over a document. The time complexity of this algorithm is not dependent on the number of terms being searched or replaced. For a document of size N (characters) and a dictionary of M keywords, the time complexity will be O(N). This algorithm is much faster than Regex, because regex time complexity is O(MxN).

[FlashText](https://arxiv.org/abs/1711.00046) is loosely based on the [Aho-Corasick Algorithm](https://cp-algorithms.com/string/aho_corasick.html), but it doesn't match substrings - only the longest complete match of a search term. The implementation allows to add a collection of search terms AND their synonyms. With those a [trie dictionary](https://en.wikipedia.org/wiki/Trie) is built. Now if you perform a search with FlashText, the algorithm would iterate over every character of the input text and if a sequence of characters match in the trie dictionary, it adds it to a list of found keywords. Given the speed and the capabilities FlashText is an good candidate.

Things that are not in the scope of FlashText:
- counting the occurances of search terms, and in general parsing the result other than listing matches
- returning the synonyms that were found, only the main keyword is returned
- data handling could be smoother
- it is set-up to bring your own data, but some data doesn't hurt either, right?

That's where **flashgeotext** comes in. :nerd_face:

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

for usage:
```bash
pip install git+https://github.com/iwpnd/flashgeotext.git
```

for development:
```bash
git clone https://github.com/iwpnd/flashgeotext.git
pip install -e toponym/
```

## Running the tests

```bash
python -m pytest flashgeotext/tests -v
```

## Authors

* **Benjamin Ramser** - *Initial work* - [iwpnd](https://github.com/iwpnd)

See also the list of [contributors](https://github.com/iwpnd/flashgeotext/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

Demo Data cities from [http://www.geonames.org](http://www.geonames.org) licensed under the Creative Commons Attribution 3.0 License.

## Acknowledgments

* Hat tip to [@vi3k6i5](https://github.com/vi3k6i5) for his [paper](https://arxiv.org/abs/1711.00046) and implementation
