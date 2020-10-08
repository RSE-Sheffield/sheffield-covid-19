# python

# Please run with python ingest.py

"""
Script to fetch HTML and data from
The University of Sheffield's
COVID-19 dashboard
"""

# https://docs.python.org/3/library/xml.etree.elementtree.html
import xml.etree

# https://requests.readthedocs.io/en/master/
import requests

# https://pypi.org/project/html5lib/
import html5lib

URL="https://www.sheffield.ac.uk/autumn-term-2020/covid-19-statistics/"

def main():
    response = requests.get(URL)
    dom = html5lib.parse(response.text, namespaceHTMLElements=False)
    things = dom.findall(".//tr")
    for thing in things:
        for el in thing:
            content = xml.etree.ElementTree.tostring(el, encoding="unicode")
            content = content.strip()
            print(content)


if __name__ == "__main__":
    main()
