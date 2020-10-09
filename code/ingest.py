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
# https://docs.python.org/3/library/argparse.html
import argparse
# https://docs.python.org/3/library/csv.html
import csv
# https://docs.python.org/3/library/json.html
import json
# https://dateutil.readthedocs.io/en/2.8.1/
import dateutil.parser
# https://pypi.org/project/html5lib/
import html5lib
# https://requests.readthedocs.io/en/master/
import requests

URL="https://www.sheffield.ac.uk/autumn-term-2020/covid-19-statistics/"


def main():
# Argument Parsing    
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', type=str, help='Store result in .CSV file', dest='csv_file', required=False)
    parser.add_argument('--json', type=str, help='Store result in .JSON file', dest='json_file', required=False)
    args = parser.parse_args()
    
    dom = fetch()

    table = extract(dom)
    validated = validate(table)
    data = transform(validated)
    for row in data:
        print(row)

# Converting output to CSV or JSON based on user input
    if args.csv_file is not None:
        file = args.csv_file
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "New staff cases", "New student cases"])
            writer.writerows(data) 
    elif args.json_file is not None:
        file = args.json_file
        with open(file, 'w') as f:
            f.write(json.dumps(data))


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
