import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from label_schema import get_label_names, validate_label


class LabelSchemaTests(unittest.TestCase):
    def test_label_schema_contains_expected_labels(self):
        labels = get_label_names()
        self.assertIn("exact_duplicate", labels)
        self.assertIn("paraphrase", labels)
        self.assertIn("related_but_not_duplicate", labels)
        self.assertIn("partial_overlap", labels)
        self.assertIn("unrelated", labels)

    def test_validate_label_accepts_known_values(self):
        self.assertTrue(validate_label("paraphrase"))
        self.assertFalse(validate_label("not_a_label"))


if __name__ == "__main__":
    unittest.main()
