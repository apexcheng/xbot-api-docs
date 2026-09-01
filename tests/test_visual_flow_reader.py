import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "project-template"
    / ".agents"
    / "skills"
    / "xbot-visual-flow-reader"
    / "scripts"
    / "inspect_visual_project.py"
)
SPEC = importlib.util.spec_from_file_location("inspect_visual_project", SCRIPT_PATH)
visual_flow_reader = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(visual_flow_reader)


class VisualFlowReaderTests(unittest.TestCase):
    def test_inventory_does_not_return_variable_values(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            package_data = {
                "startup": "main",
                "robot_type": "app",
                "flows": [
                    {"name": "main", "filename": "main", "kind": "Visual"},
                    {"name": "run", "filename": "run", "kind": "Code"},
                ],
                "variables": [
                    {"name": "account", "type": "str", "value": "secret-value"}
                ],
            }
            (project_dir / "package.json").write_text(
                json.dumps(package_data, ensure_ascii=False), encoding="utf-8"
            )
            (project_dir / "main.pybx").write_bytes(b"binary-flow")
            (project_dir / "run.py").write_text(
                "from .config import CONFIG_PATH\n\ndef main(args):\n    return args\n",
                encoding="utf-8",
            )
            (project_dir / "selectorsV2.xml").write_text(
                '<?xml version="1.0"?><repository><group><item name="登录按钮" /></group></repository>',
                encoding="utf-8",
            )
            (project_dir / "imagesV2.xml").write_text(
                '<?xml version="1.0"?><repository />', encoding="utf-8"
            )

            result = visual_flow_reader.inspect_project(project_dir)
            serialized = json.dumps(result, ensure_ascii=False)

            self.assertEqual(result["startup"], "main")
            self.assertEqual(result["variable_names"], ["account"])
            self.assertNotIn("secret-value", serialized)
            self.assertTrue(result["flows"][0]["binary"])
            self.assertEqual(result["flows"][1]["code"]["functions"][0]["name"], "main")
            self.assertEqual(result["selectors"]["count"], 2)
            self.assertEqual(result["selectors"]["names"], ["登录按钮"])


if __name__ == "__main__":
    unittest.main()
