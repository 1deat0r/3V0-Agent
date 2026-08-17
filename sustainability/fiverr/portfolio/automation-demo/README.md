# clean_orders

Dedupe an orders CSV (by id, keeping the last row) and forward-fill blank
prices from the previous row. Stdlib only — no pip install.

    python3 clean_orders.py orders.csv            # writes orders.clean.csv
    python3 clean_orders.py orders.csv -o out.csv # custom output

Fails with a clear message (not a traceback) on a missing file or empty CSV.
Run the tests with:

    python3 -m unittest test_clean_orders -v
