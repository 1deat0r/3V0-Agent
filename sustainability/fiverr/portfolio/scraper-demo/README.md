# extract_products — scraper demo

Parses product cards from a local HTML file into CSV and writes a
`validation_report.txt` saying exactly what came back empty. Stdlib only.

    python3 extract_products.py fixtures/products.html   # writes products.csv
    python3 extract_products.py page.html -o out.csv

Run the tests:

    python3 -m unittest test_extract_products -v

This is the "loud failure" pattern every scraping order ships with: the report
tells you which fields are missing and how many cards failed to parse —
never silently wrong data.
