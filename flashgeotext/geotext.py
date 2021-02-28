from typing import Optional

from pydantic import BaseModel

from flashgeotext.lookup import LookupDataPool
from flashgeotext.lookup import MissingLookupDataError


class GeoTextConfiguration(BaseModel):
    """GeoText configuration

    Args:
    use_demo_data (bool): load demo data or not, default True
    case_sensitive (bool): case sensitive lookup, default True
    """

    use_demo_data: Optional[bool] = True
    case_sensitive: Optional[bool] = True


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

    """

    def __init__(
        self, config: GeoTextConfiguration = GeoTextConfiguration().dict()
    ) -> None:
        """ instantiate an empty LookupDataPool, optionally/by default with demo data

        Args:
            config: GeoTextConfiguration = { use_demo_data: True, case_sensitive: True }.
        """
        self.pool: dict = {}

        if config["use_demo_data"]:
            self._add_demo_data(case_sensitive=config["case_sensitive"])

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
            output[lookup] = self._parse_extract(extract, span_info=span_info)

        return output

    def _parse_extract(self, extract_data: list, span_info: bool = True) -> dict:
        """Parse flashtext.KeywordProcessor.extract_keywords() output to count occurances

        Parse flashtext.KeywordProcessor.extract_keywords() output to count occurances,
        and optionally span_info.

        Args:
            extract_data (list): flashtext.KeywordProcessor.extract_keywords() return value
            span_info (bool): optionally, parse span_info

        Returns:
            parsed_extract (dict): parsed extract_data to include count, optionally span_info
        """
        parsed_extract: dict = {}

        if span_info:
            for entry in extract_data:
                if entry[0] not in parsed_extract:
                    parsed_extract[entry[0]] = {
                        "count": 1,
                        "span_info": [(entry[1], entry[2])],
                    }
                else:
                    parsed_extract[entry[0]]["count"] = (
                        parsed_extract[entry[0]]["count"] + 1
                    )
                    parsed_extract[entry[0]]["span_info"] = parsed_extract[entry[0]][
                        "span_info"
                    ] + [(entry[1], entry[2])]

        else:
            for entry in extract_data:
                if entry not in parsed_extract:
                    parsed_extract[entry] = {"count": 1}
                else:
                    parsed_extract[entry]["count"] = parsed_extract[entry]["count"] + 1

        return parsed_extract
