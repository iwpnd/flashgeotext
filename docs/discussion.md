I was approached with the question if I could extract a given set of city names from a text. At first I was like :smirk::+1:, but very quickly I noticed that the task was not as trivial as I thought it would be. :cold_sweat:

1. if you match every word in a lookup with every match in an input_text, you're left with m*n calculations.
2. if the city you're looking for consists of more than one word, you have to match against [n-grams](https://blog.xrds.acm.org/2017/10/introduction-n-grams-need/) of the input text.
3. if you happen to want to find synonyms of your city names you have to come up with a data structure to match the city name to its synonyms and vice versa
4. you're not allowed to use elasticsearch :frowning:

Let's see if there are already solution out there. I will try to evaluate some libraries against my use-case. My puny judgement doesn't mean that some are bad in general, just that they do not 100% fit my use case, that's all.

### GeoText

[GeoText](https://github.com/elyase/geotext) relies on a single regex search pattern to extract named entities from an input text. Afterwards GeoText tries to match every single one of the entities found to a collection of city and country names one by one. This approach is fast for the 22.000 cities that come with the library, but do not scale well with longer texts and more cities/keywords in a lookup file. GeoText also does not make it easy to bring your own data. Also synonyms are not in the scope of GeoText. Another problem is the regex search pattern that extracts named entities. It is a fine line between matching correctly and matching too much, and it get's even harder to match, when city names contain of more than a couple of words.

```python
from geotext import GeoText

text = "I live in Ixtapan de la Sal."
GeoText(text).cities
>> []
```

### spaCy

[spaCy](https://github.com/explosion/spaCy) is awesome. It supports a lot of languages. It's easy to learn, hard to master. It's super well documented and embedded into a great community and a great ecosystem of plugins/addons/spinoffs. It has a lot of functionality aside from named entity extraction. And it does what it is supposed to do and more. However, named entity extraction with spaCy is still based on a trained models prediction, and even though the core models perform really good, they are not 100% accurate. And to go on, even if you extract all location/cities/countries from an input text, you still have to match if you want a normalized output. There is also no support to count occurances, let alone handle synonyms. On top of that spaCy is build with C dependencies and you are limited to the pre-trained models, unless you want to train your own language model from scratch.

### FlashText

> FlashText can search or replace keywords in one pass over a document. The time complexity of this algorithm is not dependent on the number of terms being searched or replaced. For a document of size N (characters) and a dictionary of M keywords, the time complexity will be O(N). This algorithm is much faster than Regex, because regex time complexity is O(MxN).

[FlashText](https://arxiv.org/abs/1711.00046) is loosely based on the [Aho-Corasick Algorithm](https://cp-algorithms.com/string/aho_corasick.html), but it doesn't match substrings - only the longest complete match of a search term. The implementation allows to add a collection of search terms AND their synonyms. With those a [trie dictionary](https://en.wikipedia.org/wiki/Trie) is built. Now if you perform a search with FlashText, the algorithm would iterate over every character of the input text and if a sequence of characters match in the trie dictionary, it adds it to a list of found keywords. Given the speed and the capabilities FlashText is an good candidate.

Things that are not in the scope of FlashText:
- counting the occurances of search terms, and in general parsing the result other than listing matches
- returning the synonyms that were found, only the main keyword is returned
- data handling could be smoother
- it is set-up to bring your own data, but some data doesn't hurt either, right?

That's where **flashgeotext** comes in. :nerd_face:
