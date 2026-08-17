import unittest
from clean_orders import clean


class TestClean(unittest.TestCase):
    def test_dedupe_keeps_last(self):
        rows = [{"id": "1", "price": "5"}, {"id": "1", "price": "9"},
                {"id": "2", "price": "7"}]
        out = clean(rows)
        self.assertEqual([r["id"] for r in out], ["1", "2"])
        self.assertEqual(out[0]["price"], "9")  # last wins

    def test_fills_blank_price_from_previous(self):
        rows = [{"id": "1", "price": "5"}, {"id": "2", "price": ""}]
        out = clean(rows)
        self.assertEqual(out[1]["price"], "5")

    def test_blank_price_with_no_previous_defaults_to_zero(self):
        out = clean([{"id": "1", "price": ""}])
        self.assertEqual(out[0]["price"], "0")

    def test_order_preserved_by_first_appearance(self):
        rows = [{"id": "b", "price": "1"}, {"id": "a", "price": "2"},
                {"id": "b", "price": "3"}]
        out = clean(rows)
        self.assertEqual([r["id"] for r in out], ["b", "a"])
        self.assertEqual(out[0]["price"], "3")


if __name__ == "__main__":
    unittest.main()
