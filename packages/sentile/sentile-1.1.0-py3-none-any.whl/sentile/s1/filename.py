import re
import datetime
from typing import Union
from pathlib import Path
from enum import Enum


Polarization = Enum("Polarization", "VV VH")


class FileName:
    def __init__(self, path: Union[Path, str]) -> None:
        self.path = Path(path)

        pattern = (
                r"^s1[ab]-"
                r"(?P<mode>(iw|ew|wv|im))-"
                r"(?P<product>(slc|grd|ocn))-"
                r"(?P<polarization>(hh|hv|vv|vh))-"
                r"(?P<start>\d{8}T(\d{6}))-"
                r"(?P<stop>\d{8}T(\d{6}))-"
                r"(?P<orbit>(\d{6}))-"
                r"(?P<mission>[A-Z0-9]{6})-"
                r"(?P<image>[0-9]{3})"
            )

        match = re.match(pattern, self.path.name, re.IGNORECASE)

        if not match:
            raise RuntimeError(f"unable to parse file name {path}")

        self.props = match.groupdict()

    @property
    def mode(self) -> str:
        return self.props["mode"]

    @property
    def product(self) -> str:
        return self.props["product"]

    @property
    def polarization(self) -> str:
        return self.props["polarization"]

    @property
    def start(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.props["start"], "%Y%m%dT%H%M%S")

    @property
    def stop(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.props["stop"], "%Y%m%dT%H%M%S")
