"""
Basic tests for the TASK NORMALIZATION ENGINE.

Run with:
    pytest tests/test_task_normalizer.py
    # or
    python -m unittest tests/test_task_normalizer.py
"""

import unittest

from core.normalization.task_normalizer import normalize_task, NormalizedTask


class TestTaskNormalizer(unittest.TestCase):

    def test_reference_example(self):
        result = normalize_task("студия до 700$ возле моря с хорошим интернетом")
        self.assertEqual(result["type"], "studio")
        self.assertEqual(result["price_max"], 700.0)
        self.assertIsNone(result["price_min"])
        self.assertIn("sea_view", result["constraints"])
        self.assertIn("good_internet", result["constraints"])

    def test_output_schema_keys(self):
        result = normalize_task("любая квартира")
        for key in ("location", "price_min", "price_max", "type", "duration", "constraints"):
            self.assertIn(key, result)
        self.assertIsInstance(result["constraints"], list)

    def test_price_range(self):
        result = normalize_task("apartment from 300 to 700 usd")
        self.assertEqual(result["type"], "apartment")
        self.assertEqual(result["price_min"], 300.0)
        self.assertEqual(result["price_max"], 700.0)

    def test_price_dash_range(self):
        result = normalize_task("villa 500-1200$")
        self.assertEqual(result["type"], "villa")
        self.assertEqual(result["price_min"], 500.0)
        self.assertEqual(result["price_max"], 1200.0)

    def test_lower_bound_only(self):
        result = normalize_task("студию от 400$")
        self.assertEqual(result["price_min"], 400.0)
        self.assertIsNone(result["price_max"])

    def test_single_number_with_currency_is_upper_bound(self):
        result = normalize_task("studio 700$")
        self.assertEqual(result["price_max"], 700.0)

    def test_duration_months(self):
        result = normalize_task("apartment for 6 months near beach")
        self.assertEqual(result["duration"], "6m")

    def test_duration_long_term(self):
        result = normalize_task("долгосрочная аренда квартиры")
        self.assertEqual(result["duration"], "long_term")

    def test_constraints_english(self):
        result = normalize_task("villa with pool and parking and good internet")
        self.assertIn("pool", result["constraints"])
        self.assertIn("parking", result["constraints"])
        self.assertIn("good_internet", result["constraints"])

    def test_constraints_are_unique(self):
        result = normalize_task("студия интернет wifi хороший интернет")
        self.assertEqual(result["constraints"].count("good_internet"), 1)

    # --- edge cases: must never raise -------------------------------------
    def test_none_input(self):
        result = normalize_task(None)
        self.assertEqual(result, NormalizedTask().to_dict())

    def test_empty_string(self):
        result = normalize_task("")
        self.assertIsNone(result["type"])
        self.assertEqual(result["constraints"], [])

    def test_whitespace_only(self):
        result = normalize_task("      ")
        self.assertEqual(result, NormalizedTask().to_dict())

    def test_gibberish(self):
        result = normalize_task("!!!??? 123 ###")
        self.assertIsNone(result["type"])

    def test_non_string_input(self):
        result = normalize_task(12345)
        self.assertIn("constraints", result)

    # --- dict passthrough / backward compatibility ------------------------
    def test_dict_passthrough(self):
        raw = {
            "location": "Da Nang",
            "min_price": 300,
            "max_price": 700,
            "property_type": "studio",
            "constraints": ["sea_view"],
        }
        result = normalize_task(raw)
        self.assertEqual(result["location"], "Da Nang")
        self.assertEqual(result["price_min"], 300.0)
        self.assertEqual(result["price_max"], 700.0)
        self.assertEqual(result["type"], "studio")
        self.assertIn("sea_view", result["constraints"])

    def test_dict_string_constraint_coerced_to_list(self):
        result = normalize_task({"constraints": "pool"})
        self.assertEqual(result["constraints"], ["pool"])

    def test_normalized_task_to_dict(self):
        task = NormalizedTask(location="Bali", type="villa")
        d = task.to_dict()
        self.assertEqual(d["location"], "Bali")
        self.assertEqual(d["type"], "villa")


if __name__ == "__main__":
    unittest.main()
