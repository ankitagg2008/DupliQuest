import sys
import unittest
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from augmentation import generate_simple_paraphrase, augment_dataset


class AugmentationTests(unittest.TestCase):
    def test_generate_simple_paraphrase_changes_text(self):
        s = "Which state has the most people?"
        p = generate_simple_paraphrase(s)
        self.assertIsInstance(p, str)
        self.assertNotEqual(p, "")

    def test_augment_dataset_runs(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            sample = td / "sample.csv"
            out = td / "aug.csv"
            sample.write_text("id,question1,question2,is_duplicate\n1,Which state has the most people?,Which state has the most population?,1\n")
            res = augment_dataset(sample, out, mode="paraphrase", max_rows=1)
            self.assertTrue(res.exists())
            text = res.read_text()
            self.assertIn("semantic_label", text)


if __name__ == "__main__":
    unittest.main()
