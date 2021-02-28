# Table of Contents

* [flashgeotext.lookup](#flashgeotext.lookup)
  * [LookupDuplicateError](#flashgeotext.lookup.LookupDuplicateError)
  * [MissingLookupDataError](#flashgeotext.lookup.MissingLookupDataError)
  * [LookupValidation](#flashgeotext.lookup.LookupValidation)
  * [LookupData](#flashgeotext.lookup.LookupData)
    * [validate](#flashgeotext.lookup.LookupData.validate)
  * [LookupDataPool](#flashgeotext.lookup.LookupDataPool)
    * [add](#flashgeotext.lookup.LookupDataPool.add)
    * [remove](#flashgeotext.lookup.LookupDataPool.remove)
    * [remove\_all](#flashgeotext.lookup.LookupDataPool.remove_all)
  * [load\_data\_from\_file](#flashgeotext.lookup.load_data_from_file)

<a name="flashgeotext.lookup"></a>
# flashgeotext.lookup

<a name="flashgeotext.lookup.LookupDuplicateError"></a>
## LookupDuplicateError Objects

```python
class LookupDuplicateError(Exception)
```

Exception is raised if LookupData is already in LookupDataPool

**Arguments**:

- `message` _str_ - Human readable string describing the exception.


**Attributes**:

- `message` _str_ - Human readable string describing the exception.

<a name="flashgeotext.lookup.MissingLookupDataError"></a>
## MissingLookupDataError Objects

```python
class MissingLookupDataError(Exception)
```

Exception is raised if GeoText.extract() is used on empty LookupDataPool

**Arguments**:

- `message` _str_ - Human readable string describing the exception.


**Attributes**:

- `message` _str_ - Human readable string describing the exception.

<a name="flashgeotext.lookup.LookupValidation"></a>
## LookupValidation Objects

```python
class LookupValidation()
```

Data validation container object

**Arguments**:

- `status` _str_ - Humanreadible string containing the Error status.
- `error_count` _int_ - Error count in validation data.
  errors (dict):

- `Example` - {
- `"Berlin"` - [
  "Berlin missing in list of synonyms",
  "data['Berlin'] is not a list of synonyms"
  ]
  }


**Arguments**:

- `status` _str_ - Humanreadible string containing the Error status.
- `error_count` _int_ - Error count in validation data.
  errors (dict):

- `Example` - {
- `"Berlin"` - [
  "Berlin missing in list of synonyms",
  "data['Berlin'] is not a list of synonyms"
  ]
  }

<a name="flashgeotext.lookup.LookupData"></a>
## LookupData Objects

```python
class LookupData(BaseModel,  object)
```

Data that is supposed to be looked up in a text

Setting a script here would add characters of that script (see resources/scripts.json)
to the set of non_word_boundaries's default of:
>> {'k', '6', 's', 'M', 'i', 'S', 'm', 'E', 'r', 'W', 'v', 'l',
'R', 'f', 'e', 'X', '7', '3', 'q', 'w', '0', 'x', 'V', 'C', 'n',
'I', '4', 'D', 'z', 'G', 'L', '2', 'T', 'U', '_', 'B', 't', 'Q',
'd', '9', 'h', 'o', 'c', 'u', 'P', 'K', 'Y', 'p', 'A', 'J', 'O',
'N', 'H', 'j', 'a', 'Z', '5', '1', 'b', 'y', 'F', '8', 'g'}

**Arguments**:

- `name` _pydantic.StrictStr_ - Human readable name as string describing the data.
- `data` _dict_ - dictionary containing data to lookup and their synonyms
- `script` - (pydantic.StrictStr): what scripts characters to add to non_word_boundaries


**Attributes**:

- `name` _pydantic.StrictStr_ - Human readable name as string describing the data.
- `data` _dict_ - dictionary containing data to lookup and their synonyms
- `script` - (pydantic.StrictStr): what scripts characters to add to non_word_boundaries

<a name="flashgeotext.lookup.LookupData.validate"></a>
#### validate

```python
 | validate() -> dict
```

Validate if data attribute has appropiate structure.

returns:
    LookupValidation

<a name="flashgeotext.lookup.LookupDataPool"></a>
## LookupDataPool Objects

```python
class LookupDataPool()
```

Collection of KeywordProcessors from LookupData

**Arguments**:

- `pool` _dict_ - Collection of LookupData.


**Attributes**:

- `pool` _dict_ - Collection of LookupData.


**Example**:

  pool = {
- `LookupData.name` - flashtext.KeywordProcessor.add_keywords_from_dict(LookupData.data)
  }

<a name="flashgeotext.lookup.LookupDataPool.add"></a>
#### add

```python
 | add(lookup: LookupData, update: bool = False) -> None
```

Add LookupData to LookupDataPool

Add LookupData to LookupDataPool.
Raises flashgeotext.lookup.LookupDuplicateError if lookup
is already in pool unless update == True.

**Arguments**:

- `lookup` _LookupData_ - LookupData to add to pool
- `update` _bool_ - Allow update of an existing entry in LookupDataPool

<a name="flashgeotext.lookup.LookupDataPool.remove"></a>
#### remove

```python
 | remove(lookup_to_remove: str) -> None
```

Remove LookupData from LookupDataPool

**Arguments**:

- `lookup_to_remove` _str_ - LookupData to remove from pool

<a name="flashgeotext.lookup.LookupDataPool.remove_all"></a>
#### remove\_all

```python
 | remove_all()
```

Remove all LookupData from LookupDataPool

<a name="flashgeotext.lookup.load_data_from_file"></a>
#### load\_data\_from\_file

```python
load_data_from_file(file: str) -> dict
```

Load data from json file

Load data from json file. Raises TypeError if not json

**Arguments**:

- `file` _str_ - path to file
