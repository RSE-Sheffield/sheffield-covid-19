import json

from code.ingest import extract_transform_data

"""
todo:
check requirements.txt still valid by deleting/readding env
any potential issues with eval?
what happens when stuff that needs the dom response needs to be tested?
useful to have snapshots as fixtures or just overcomplicated for no reason?
get ci to run tests
more tests!
"""


def test_extract_transform_data():
    with open("tests/state_snapshot/website_snapshot_20201026.html") as snapshot_file:
        html_input = snapshot_file.read()

    with open("tests/state_snapshot/data_snapshot_20201026.json") as snapshot_file:
        expected_output = json.loads(snapshot_file.read())

    transformed_output = extract_transform_data(html_input)

    assert transformed_output == expected_output
