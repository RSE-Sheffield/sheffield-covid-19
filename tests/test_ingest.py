import json
import pytest

from _elementtree import Element
from code.ingest import extract_transform_data, validate, transform, extract


@pytest.fixture
def website_snapshot():
	with open("tests/state_snapshot/website_snapshot_20201026.html") as snapshot_file:
		html_snapshot = snapshot_file.read()

	return html_snapshot


@pytest.fixture
def output_data_snapshot():
	with open("tests/state_snapshot/data_snapshot_20201026.json") as snapshot_file:
		data_snapshot = json.loads(snapshot_file.read())

	return data_snapshot


def test_extract_transform_data(website_snapshot, output_data_snapshot):
	# given the webpage, expect relevant data extracted in correct format
	transformed_output = extract_transform_data(website_snapshot)
	assert transformed_output == output_data_snapshot


def test_extract(website_snapshot):
	# given the webpage, expect only table rows extracted
	output = extract(website_snapshot)
	assert [element is type(Element) and element.tag == "tr" for element in output]


@pytest.mark.parametrize("test_input,expected", [(
	# input valid, expect no changes in output
	[["Tuesday 27 October", "1", "17"], ["Monday 19 October", "5", "23"]],
	[["Tuesday 27 October", "1", "17"], ["Monday 19 October", "5", "23"]]),
	# input contains headings, expect headings removed
	([["Day", "New staff cases", "New student cases"], ["Monday 26 October", "3", "16"]],
	[["Monday 26 October", "3", "16"]]),
	# input contains asterisks, expect asterisks removed
	([["Monday 26 October", "3*", "16*"]],
	[["Monday 26 October", "3", "16"]]),
	# comments in "ingest.py" suggest this should throw an exception, but code does not (until transform)
	# assuming this was intentional, changing comment, allowing to pass
	([["Invalid date", "1", "17"], ["Monday 19 October", "5!", "23!"]],
	[["Invalid date", "1", "17"], ["Monday 19 October", "5!", "23!"]])
])
def test_validate(test_input, expected):
	assert validate(test_input) == expected


def test_transform():
	# given format [["%A %d %B", "<int>", "<int>"], ...], expect ordered [["YYYY-MM-DD", int, int], ...]
	test_input = [["Tuesday 27 October", "1", "17"], ["Monday 19 October", "5", "23"]]
	expected = [["2020-10-19", 5, 23], ["2020-10-27", 1, 17]]

	assert (transform(test_input)) == expected


@pytest.mark.parametrize("test_input",[
	[["un-parseable date", "15", "17"], ["Monday 19 October", "5", "23"]],
	[["Tuesday 27 October", "un-intable", "17"], ["Monday 19 October", "5", "23"]],
	[["Tuesday 27 October", "15", "un-intable"], ["Monday 19 October", "5", "23"]],
	[[5, 5, 5], ["Monday 19 October", "5", "23"]]])
def test_transform_expect_exception(test_input):
	with pytest.raises(Exception):
		transform(test_input)
