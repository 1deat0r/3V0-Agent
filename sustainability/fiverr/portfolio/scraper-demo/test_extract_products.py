import unittest
from extract_products import ProductParser, validation_report


class TestProductParser(unittest.TestCase):
    def test_extracts_complete_cards(self):
        html = """
        <div class="product-card">
          <h2 class="product-name">A</h2><span class="price">$1</span>
          <a class="product-link" href="/a">x</a>
          <span class="availability">In stock</span>
        </div>"""
        p = ProductParser()
        p.feed(html)
        self.assertEqual(len(p.products), 1)
        self.assertEqual(p.products[0]["name"].strip(), "A")
        self.assertEqual(p.products[0]["price"], "$1")

    def test_counts_cards_seen(self):
        html = '<div class="product-card"></div><div class="product-card"></div>'
        p = ProductParser()
        p.feed(html)
        self.assertEqual(p.cards_seen, 2)

    def test_validation_report_flags_empty_fields(self):
        products = [{"name": "A", "price": "", "link": "/a", "availability": ""}]
        r = validation_report(products, cards_seen=1, source="x.html")
        self.assertIn("price        : 1", r)
        self.assertIn("availability : 1", r)

    def test_validation_report_warns_on_failed_cards(self):
        r = validation_report([], cards_seen=2, source="x.html")
        self.assertIn("WARNING: 2 card(s) failed to parse", r)


if __name__ == "__main__":
    unittest.main()
