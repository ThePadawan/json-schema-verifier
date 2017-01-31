
import unittest
import glob
from jsonschema import SchemaError

from validate.validate import main, get_error, inspect

class AllTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output = []

    def testNoArgumentSpecified(self):
        main([], self.do_print)

    def testNonFolderSpecified(self):
        main(["main.py", "nonfolder"], self.do_print)

    def testIncorrectSchema(self):
        # required should have an array as value.
        # Specifying an object should fail.
        error = get_error("{\"required\": {}}")
        self.assertIsNotNone(error)
        self.assertIsInstance(error, SchemaError)

    def testIncorrectJson(self):
        error = get_error("{{}")
        self.assertIsNotNone(error)
        self.assertIsInstance(error, ValueError)

    def testCorrectSchema(self):
        error = get_error("{}")
        self.assertIsNone(error)

    def testZeroFiles(self):
        inspect([], self.do_print)

    def testValidFolder(self):
        try:
            main(["main.py", "test/test_schema"], self.do_print)
        except SystemExit:
            pass

    def do_print(self, msg):
        self.output.append(msg)