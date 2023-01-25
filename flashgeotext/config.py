from pydantic import BaseModel


class GeoTextConfiguration(BaseModel):
    """GeoText configuration

    Args:
    use_demo_data (bool): load demo data or not, default True
    case_sensitive (bool): case sensitive lookup, default True
    """

    use_demo_data: bool = True
    case_sensitive: bool = True


config = GeoTextConfiguration()
