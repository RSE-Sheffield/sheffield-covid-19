# python

# Please run with python ingest.py

"""
Script to fetch HTML and data from
The University of Sheffield's
COVID-19 dashboard

The flow is approximately:
- fetch, HTML from webapge (requests)
- extract, rows from HTML (html5lib/xpath)
- validate, rows as being data in expected format
- transform, data into a more regular model
- store, data as CSV and/or JSON
"""

# https://docs.python.org/3/library/xml.etree.elementtree.html
import xml.etree

# https://dateutil.readthedocs.io/en/2.8.1/
import dateutil.parser
# https://pypi.org/project/html5lib/
import html5lib
# https://requests.readthedocs.io/en/master/
import requests

URL="https://www.sheffield.ac.uk/autumn-term-2020/covid-19-statistics/"


def main():
    dom = fetch()

    table = extract(dom)
    validated = validate(table)
    data = transform(validated)
    for row in data:
        print(row)


def transform(rows):
    """
    The input is a list of rows, each row is a list of strings.
    The return value is a list of rows, each row is a list of
    data values.
    Dates in the first cell, are transformed into ISO 8601 date
    strings of the form YYYY-MM-DD;
    Numbers in subsequent cells, are transformed into int.

    For your convenience, the output is sorted.
    """

    result = []
    for row in rows:
        iso_date = str(dateutil.parser.parse(row[0]).date())
        out = [iso_date]
        out.extend(int(x) for x in row[1:])
        result.append(out)

    return sorted(result)


def extract(dom):
    """
    Extract all the rows that plausibly contain data,
    and return them as a list of list of strings.
    """

    rows = dom.findall(".//tr")

    result = []
    for row in rows:
        result.append([el.text for el in row])

    return result


def fetch():
    """
    Fetch the web page and return it as a parsed DOM object.
    """

    response = requests.get(URL)
    dom = html5lib.parse(response.text, namespaceHTMLElements=False)

    return dom


def validate(table):
    """
    `table` should be a table of strings in list of list format.
    Each row is checked to see if it is of the expected format.
    A fresh table is returned (some rows are removed because
    they are "metadata").
    Invalid inputs will result in an Exception being raised.
    """

    validated = []

    for row in table:
        if "Day" in row[0]:
            assert "New staff" in row[1]
            assert "New student" in row[2]
            continue
        validated.append(row)

    return validated


if __name__ == "__main__":
    main()
