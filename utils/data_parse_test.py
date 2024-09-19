# -*- coding: utf-8 -*-
import unittest
import logging
from .data_parse import DataParse


class TestDataParseInit(unittest.TestCase):
    def setUp(self) -> None:
        self.log = logging.getLogger(__name__)

    def test_init_with_dict(self):
        data = {"key": "value"}
        dp = DataParse(data)
        self.assertIsInstance(dp, DataParse)
        self.assertEqual(dp.data, data)

    def test_init_with_non_dict(self):
        data = [1, 2, 3]
        with self.assertRaises(ValueError):
            DataParse(data)

    def test_parse_valid_value(self):
        data = {"key": "value"}
        parser = DataParse(data)
        assert parser.parse("key", str) == "value"

    def xtest_parse_nonexistent_key(self):
        data = {"key": "value"}
        parser = DataParse(data)
        with self.assertRaises(ValueError, "not found another_key in {'key': 'value'}"):
            parser.parse("another_key", str)

    def xtest_parse_invalid_type(self):
        data = {"key": 1}
        parser = DataParse(data)
        with self.assertRaises(
            ValueError, "invalid type  for key 1, expected <class 'str'> got (<class 'int'>)"
        ):  # noqa: E501.raises(ValueError, match="invalid type  for key 1, expected <class 'str'> got (<class 'int'>)"):
            parser.parse("key", str)

    def xtest_parse_default_value(self):
        data = {}
        parser = DataParse(data)
        assert parser.parse("key", str, "default") == "default"


if __name__ == "__main__":
    unittest.main()
