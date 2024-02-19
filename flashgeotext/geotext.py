from typing import Dict, List, Tuple

from pydantic import BaseModel

from flashgeotext.config import GeoTextConfiguration, config
from flashgeotext.lookup import LookupDataPool, MissingLookupDataError


class ExtractMeta(BaseModel):
    count: int
    span_info: List[Tuple[int, int]]
    found_as: List[str]


class Extract:
    data: Dict[str, ExtractMeta] = {}

    def __init__(self) -> None:
        self.data = {}

    def has_name(self, name: str) -> bool:
        return name in self.data

    def add(self, name: str, meta: ExtractMeta) -> None:
        self.data[name] = meta

    def add_span(self, name: str, span: Tuple[int, int]) -> None:
        if not self.has_name(name):
            return

        self.data[name].span_info.append(span)

    def add_found_as(self, name: str, found_as: str) -> None:
        if not self.has_name(name):
            return

        self.data[name].found_as.append(found_as)

    def increment_count(self, name: str) -> None:
        if not self.has_name(name):
            return

        self.data[name].count += 1

    def to_dict(self) -> Dict[str, Dict]:
        return {k: v.model_dump() for k, v in self.data.items()}


class GeoText(LookupDataPool):
    """Extract LookupData from input text

    GeoText inherits from LookupDataPool. It iterates through
    a LookupDataPool and interfaces flashtext.KeywordProcessor
    to extract keywords from an input text. It parses the result of
    flashtext.KeywordProcessor.extract_keywords() by counting the
    occurances of a LookupData point and optionally lists the
    span info.

    Example:
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
                    'span_info': [(0, 8), (45, 53)]
                    'found_as': ['Shanghai', 'Shanghai']
                    },
                'Washington, D.C.': {
                    'count': 1,
                    'span_info': [(175, 185)]
                    'found_as': ['Washington']
                    }
                },
            'countries': {
                'China': {
                    'count': 1,
                    'span_info': [(64, 69)]
                    'found_as': ['China']
                    },
                'United States': {
                    'count': 1,
                    'span_info': [(171, 173)]
                    'found_as': ['US']
                    }
                }
            }

    ```

    """

    def __init__(self, config: GeoTextConfiguration = config) -> None:
        """instantiate an empty LookupDataPool, optionally/by default with demo data

        Args:
            config: GeoTextConfiguration = { use_demo_data: True, case_sensitive: True }.
        """
        self.pool: dict = {}

        if config.use_demo_data:
            self._add_demo_data(case_sensitive=config.case_sensitive)

    def extract(self, input_text: str, span_info: bool = True) -> dict:
        """Extract LookupData from an input_text

        Args:
            input_text (str): String to extract LookupData from.
            span_info (bool): Optionally, return span_info. Defaults to True.

        Returns:
            extract_ouput (dict): dictionary of extracted LookupData entities with count
                                  and optionally with listed span info.

        """
        if not self.pool:
            raise MissingLookupDataError(
                "Empty LookupDataPool. use .add(LookupData) to add data."
            )

        output: dict = {}

        for lookup in self.pool.keys():
            extract = self.pool[lookup].extract_keywords(
                input_text, span_info=span_info
            )
            output[lookup] = self.__parse_extract(extract, input_text)

        return output

    def __parse_extract(self, extract_data: list, input_text: str) -> dict:
        """Parse flashtext.KeywordProcessor.extract_keywords() output to count occurances

        Parse flashtext.KeywordProcessor.extract_keywords() output to count occurances,
        and optionally span_info.

        Args:
            extract_data (list): flashtext.KeywordProcessor.extract_keywords() return value
            input_text (str): input text

        Returns:
            result (dict): parsed extract_data to include count, optionally span_info
        """

        result = Extract()

        for extract in extract_data:
            name = extract[0]
            span_start: int = extract[1]
            span_end: int = extract[2]

            if not result.has_name(name):
                result.add(
                    name,
                    ExtractMeta(
                        **{
                            "count": 1,
                            "span_info": [(span_start, span_end)],
                            "found_as": [input_text[span_start:span_end]],
                        }
                    ),
                )
            else:
                result.increment_count(name)
                result.add_span(name, (span_start, span_end))
                result.add_found_as(name, input_text[span_start:span_end])

        return result.to_dict()
