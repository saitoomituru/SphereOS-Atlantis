import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class M6xxLayoutTestCase(unittest.TestCase):
    def load_registry(self, relative_path: str) -> dict:
        return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))

    def test_packageとproductの置場が実在する(self) -> None:
        package_registry = self.load_registry("packages/registry.json")
        product_registry = self.load_registry("products/registry.json")

        entries = package_registry["packages"] + product_registry["products"]
        ids = [entry["id"] for entry in entries]

        self.assertEqual(len(ids), len(set(ids)))
        for entry in entries:
            self.assertTrue((ROOT / entry["path"]).is_dir(), entry["path"])
            self.assertTrue((ROOT / entry["path"] / "README.ja.md").is_file(), entry["path"])

    def test_scaffoldをruntime実装済みへ昇格しない(self) -> None:
        package_registry = self.load_registry("packages/registry.json")
        product_registry = self.load_registry("products/registry.json")

        self.assertEqual(package_registry["roadmap_coordinate"], "m.6xx.1-candidate")
        self.assertEqual(product_registry["roadmap_coordinate"], "m.6xx.1-candidate")
        self.assertEqual(
            {product["engineering_state"] for product in product_registry["products"]},
            {"NOT_IMPLEMENTED"},
        )

    def test_provider課金とOAE権限を誤所有しない(self) -> None:
        package_registry = self.load_registry("packages/registry.json")
        product_registry = self.load_registry("products/registry.json")

        adapters = next(
            package for package in package_registry["packages"] if package["id"] == "provider-adapters"
        )
        code = next(product for product in product_registry["products"] if product["id"] == "spheredos-code")

        self.assertIn("provider-payment", adapters["must_not_own"])
        self.assertIn("provider-auth", adapters["must_not_own"])
        self.assertIn("oae-commit-authority", code["must_not_own"])


if __name__ == "__main__":
    unittest.main()
