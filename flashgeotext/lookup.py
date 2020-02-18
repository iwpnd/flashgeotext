from pydantic import BaseModel


class LookupData(BaseModel):
    name: str
    data: dict


class LookupDataProcessor:
    pass
