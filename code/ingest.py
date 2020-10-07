# python

# Please run with python ingest.py

"""
Script to fetch HTML and data from
The University of Sheffield's
COVID-19 dashboard
"""

# https://requests.readthedocs.io/en/master/
import requests
# https://pypi.org/project/html5lib/
import html5lib

URL="https://www.sheffield.ac.uk/autumn-term-2020/covid-19-statistics/"

def main():
    response = requests.get(URL)
    dom = html5lib.parse(response.text,
        namespaceHTMLElements=False)
    things = dom.findall(".//{}td")
    print(things)

if __name__ == "__main__":
    main()
