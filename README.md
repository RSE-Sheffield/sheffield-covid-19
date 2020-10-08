# sheffield-covid-19

Scrape COVID-19 data from the University website.

The best target page to scrape is: https://www.sheffield.ac.uk/autumn-term-2020/covid-19-statistics

This is currently in development.

After installing Python requirements (see below),
run the code:

    python code/ingest.py


# Installing the development edition

Please create a conda environment:

    conda create --name sheffield-covid-19 python=3

activate this environment:

    conda activate sheffield-covid-19

install the remaining Python packages:

    pip install -r requirements.txt
