# flashgeotext.lookup

## LookupDuplicateError
```python
LookupDuplicateError(self, message: str)
```
Exception is raised if LookupData is already in LookupDataPool

Args:
    message (str): Human readable string describing the exception.

Attributes:
    message (str): Human readable string describing the exception.

## MissingLookupDataError
```python
MissingLookupDataError(self, message: str)
```
Exception is raised if GeoText.extract() is used on empty LookupDataPool

Args:
    message (str): Human readable string describing the exception.

Attributes:
    message (str): Human readable string describing the exception.

## LookupValidation
```python
LookupValidation(self, status: str = 'No errors detected', error_count: int = 0, errors: dict = {})
```
Data validation container object

Args:
    status (str): Humanreadible string containing the Error status.
    error_count (int): Error count in validation data.
    errors (dict):

    Example: {
        "Berlin": [
            "Berlin missing in list of synonyms",
            "data['Berlin'] is not a list of synonyms"
            ]
        }

Arguments:
    status (str): Humanreadible string containing the Error status.
    error_count (int): Error count in validation data.
    errors (dict):

    Example: {
        "Berlin": [
            "Berlin missing in list of synonyms",
            "data['Berlin'] is not a list of synonyms"
            ]
        }

## LookupData
```python
LookupData(__pydantic_self__, **data: Any) -> None
```
Data that is supposed to be looked up in a text

Args:
    name (pydantic.StrictStr): Human readable name as string describing the data.
    data (dict): dictionary containing data to lookup and their synonyms

Attributes:
    name (pydantic.StrictStr): Human readable name as string describing the data.
    data (dict): dictionary containing data to lookup and their synonyms

### validate
```python
LookupData.validate(self) -> dict
```
Validate if data attribute has appropiate structure.

returns:
    LookupValidation

## LookupDataPool
```python
LookupDataPool(self) -> None
```
Collection of KeywordProcessors from LookupData

Args:
    pool (dict): Collection of LookupData.

Attributes:
    pool (dict): Collection of LookupData.

Example:
    pool = {
        LookupData.name: flashtext.KeywordProcessor.add_keywords_from_dict(LookupData.data)
        }

### add
```python
LookupDataPool.add(self, lookup: flashgeotext.lookup.LookupData, update: bool = False) -> None
```
Add LookupData to LookupDataPool

Add LookupData to LookupDataPool.
Raises flashgeotext.lookup.LookupDuplicateError if lookup
is already in pool unless update == True.

Args:
    lookup (LookupData): LookupData to add to pool
    update (bool): Allow update of an existing entry in LookupDataPool

### remove
```python
LookupDataPool.remove(self, lookup_to_remove: str) -> None
```
Remove LookupData from LookupDataPool

Args:
    lookup_to_remove (str): LookupData to remove from pool

### remove_all
```python
LookupDataPool.remove_all(self)
```
Remove all LookupData from LookupDataPool

## load_data_from_file
```python
load_data_from_file(file: str) -> dict
```
Load data from json file

Load data from json file. Raises TypeError if not json

Args:
    file (str): path to file
