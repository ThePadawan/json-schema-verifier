# coding=utf-8
import sys
import os
from os.path import isdir, join
import json
from jsonschema import Draft4Validator, SchemaError


def get_error(schema_text):
    try:
        schema_object = json.loads(schema_text)
        Draft4Validator.check_schema(schema_object)
    except SchemaError as schema_error:
        return schema_error
    except ValueError as value_error:
        return value_error
    return None


def inspect(filenames, do_print):
    has_any_errors = False
    inspected_schema_count = 0
    for schema_filename in filenames:
        with open(schema_filename, 'r') as schema_file:
            maybe_error = get_error(schema_file.read())
            if maybe_error is not None:
                do_print("File {} has schema error: {}"
                         .format(schema_filename, maybe_error))
                has_any_errors = True
            inspected_schema_count = inspected_schema_count + 1

    if not has_any_errors:
        do_print("No schema errors found ({} inspected)"
                 .format(inspected_schema_count))

    return has_any_errors


def main(argv, do_print):
    if len(argv) < 2:
        do_print("Please specify a folder to validate.")
        return

    folder_name = argv[1]
    is_directory = isdir(folder_name)

    if not is_directory:
        do_print("The path {} is not a directory.".format(folder_name))
        return

    schema_filenames = [join(folder_name, x) for x in os.listdir(folder_name)]

    has_errors = inspect(schema_filenames, do_print)
    if has_errors:
        sys.exit(1)
