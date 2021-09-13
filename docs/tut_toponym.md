# Tutorial: How to extract toponyms from newspaper articles

In Slavic languages a word can change, depending on how and where it is used within a sentence. The city `Москва` (Moscow) changes to `Москве` when used prepositional. So when you want to eg. know if a newspaper article is talking about Moscow and do something like

```
"Москва" in "В Москве с начала года отремонтировали 3 тысячи подъездов"

>> False
```

even though the article is mentioning Moscow.

This little tutorial will quickly show you how you can work around that issue. We will be using `newspaper3k` ([github](https://github.com/codelucas/newspaper)) to extract an article text from [The Moscow Times](https://www.themoscowtimes.com/). Then we will create toponyms using `toponyms` ([github](https://github.com/iwpnd/toponym)) library and search the article text for city name mentions using `flashgeotext` ([github](https://github.com/iwpnd/flashgeotext)).

## Download and extract an article with newspaper3k

```python
from newspaper import Article

url = "https://www.themoscowtimes.com/ru/2020/04/21/v-moskve-zhenschina-umerla-na-ulichnoi-skameike-posle-otritsatelnogo-testa-na-koronavirus-a125"

article = Article(url=url, language="ru")
article.download()
article.parse()
```

This instantiate an article object, download the article at the given url and will dechrome the html to parse the actual article text.


```python
print(article.text)

>> 'Оригинал этой статьи был опубликован 20 апреля в англоязычной версии сайта The Moscow Times.\n\nКак сообщается, власти Москвы расследуют смерть женщины на скамейке возле ее дома - в день, когда она была выписана после тестирования на коронавирус.\n\nВидеозапись, предоставленная российским телеканалом REN TV, показала, что женщина, которую опознали как 48-летнюю Елену Чуклову, оставалась на скамейке, пока социальные работники и соседи пытались, но так и не смогли проникнуть в ее квартиру. Телеканал сообщил, что Следственный комитет России начал расследование сообщения о смерти женщины.\n\n«У входа женщина почувствовала плохо, социальные работники немедленно вызвали скорую помощь, — говорится в заявлении департамента здравоохранения мэрии Москвы. — Скорая помощь прибыла через 11 минут и, к сожалению, констатировала смерть».\n\nМинистерство здравоохранения сообщило, что женщина умерла в субботу, на следующий день после того, как ее госпитализировали с подозрением на пневмонию. Тогда ее имя не называлось.\n\nКак сообщили в департаменте здравоохранения, вскрытие показало, что женщина умерла от острой сердечной недостаточности. Было отмечено, что у нее была кардиомиопатия, заболевание сердечной мышцы, которое может привести к сердечной недостаточности, и «выраженные изменения в органах алкогольного происхождения».'
```

For good measure we will remove the newlines and add the `article.title` to the text we want to search for city mentions.

```python
text = article.title + " - " + article.text
text = " ".join(text.split())

>> 'В Москве женщина умерла на уличной скамейке после отрицательного теста на коронавирус - Оригинал этой статьи был опубликован 20 апреля в англоязычной версии сайта The Moscow Times. Как сообщается, власти Москвы расследуют смерть женщины на скамейке возле ее дома - в день, когда она была выписана после тестирования на коронавирус. Видеозапись, предоставленная российским телеканалом REN TV, показала, что женщина, которую опознали как 48-летнюю Елену Чуклову, оставалась на скамейке, пока социальные работники и соседи пытались, но так и не смогли проникнуть в ее квартиру. Телеканал сообщил, что Следственный комитет России начал расследование сообщения о смерти женщины. «У входа женщина почувствовала плохо, социальные работники немедленно вызвали скорую помощь, — говорится в заявлении департамента здравоохранения мэрии Москвы. — Скорая помощь прибыла через 11 минут и, к сожалению, констатировала смерть». Министерство здравоохранения сообщило, что женщина умерла в субботу, на следующий день после того, как ее госпитализировали с подозрением на пневмонию. Тогда ее имя не называлось. Как сообщили в департаменте здравоохранения, вскрытие показало, что женщина умерла от острой сердечной недостаточности. Было отмечено, что у нее была кардиомиопатия, заболевание сердечной мышцы, которое может привести к сердечной недостаточности, и «выраженные изменения в органах алкогольного происхождения».'
```

## Create the toponyms

Now we create toponyms for `Москва` using [toponyms](https://github.com/iwpnd/toponym).

```python
from toponym.recipes import Recipes
from toponym.toponym import Toponym

recipes = Recipes()
recipes.load_from_language(language="russian")

t = Toponym("Москва", recipes)
t.build()
```

Toponyms are stored in

```python
t.toponyms
>> {'nominative': ['Москва'],
 'genitive': ['Москвы', 'Москви'],
 'dative': ['Москве'],
 'accusative': ['Москву'],
 'instrumental': ['Москвой'],
 'prepositional': ['Москве']}
```

To use toponyms with [flashgeotext](https://github.com/iwpnd/flashgeotext) they have to adhere another structure.

```python
t.list_toponyms()

>> ['Москвой', 'Москвы', 'Москве', 'Москву', 'Москви', 'Москва']

lookup = {
    "Москва": t.list_toponyms()
    }
print(lookup)
>> {'Москва': ['Москвой', 'Москвы', 'Москве', 'Москву', 'Москви', 'Москва']}
```

If you want to lookup more than just one city, you would create toponyms in a loop, and store them in a dictionary like so:

```python
list_of_cities = ["Москва", "Ростов"]

lookup = dict()

for city in list_of_cities:
    t = Toponym(input_word=city, recipes=recipes)
    t.build()
    lookup[city] = t.list_toponyms()

print(lookup)

>> {
    'Москва': [
        'Москвой', 'Москвы', 'Москве',
        'Москву', 'Москви', 'Москва'
        ],
    'Ростов': [
        'Ростовя', 'Ростовю', 'Ростов',
        'Ростовем', 'Ростова', 'Ростовом',
        'Ростову', 'Ростове'
        ]
    }
```

## Extract city mentions from the article text

Now that we have a collection of toponyms, we can use [flashgeotext](https://github.com/iwpnd/flashgeotext) to extract the city mentions from the article text.

First we instantiate a Lookup with flashgeotext

```python
from flashgeotext.lookup import LookupData

city_lookup = LookupData(name="city_names", data=lookup, script="cyrillic")
```

By default `LookupData` will expect you to look for words with latin characters. So we have to specificly add `cyrillic` characters here. Then we instantiate an instance of `GeoText` while explicitly not using the demo data that comes with it, but with our own data lookup.

```python
from flashgeotext.geotext import GeoText, GeoTextConfiguration

config = GeoTextConfiguration(**{"use_demo_data": False})
geotext = GeoText(config)
geotext.add(lookup_city)
```

Now we use the `extract` method of `GeoText` to extract city mentions from a newspaper article.

```python
geotext.extract(text)

>> {
    'city_names': {
        'Москва': {
            'count': 2,
            'span_info': [(2, 8), (204, 210)]
						'found_as': ['Москве','Москвы']
            }
        }
    }
```

And there you have it. Moscow is mention two times in the article. Flashgeotext scales pretty great with increasing number of cities to look up ([read here](https://iwpnd.pw/articles/2020-02/flashgeotext-library)). So you could create a pipeline that would extract city mentions from a stream of newspaper articles in your framework of choice.
