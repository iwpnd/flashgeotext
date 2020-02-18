from flashgeotext.lookup import LookupDataPool
from flashgeotext.lookup import MissingLookupDataError


class GeoText(LookupDataPool):
    def __init__(self, use_demo_data: bool = True) -> None:
        self.pool: dict = {}

        if use_demo_data:
            self._add_demo_data()

    def extract(self, input_text: str, span_info: bool = True) -> dict:
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
