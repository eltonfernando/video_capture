# -*- coding: utf-8 -*-
from logging import getLogger


class DataParse:
    def __init__(self, data: dict) -> None:
        self.log = getLogger(__name__)
        assert isinstance(data, dict), f"expected dict, received {type(data)} value {data}"
        self.data = data

    def parse(self, key: str, type_expected: type, default: any = None) -> any:
        value = self.data.get(key, default)
        if value is None:
            raise ValueError(f"not found {key} in {self.data}")

        if not isinstance(value, type_expected):
            raise ValueError(f"invalid type  for {key} {value}, expected {type_expected} got ({type(value)})")
        if value == default:
            self.log.warning(f"Cannot parse {key}, using default {default}")
        return value
