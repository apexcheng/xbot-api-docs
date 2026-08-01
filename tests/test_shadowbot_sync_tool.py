import contextlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import shadowbot_sync_tool


class PrepareCommandTests(unittest.TestCase):
    def write_package_json(self, project_dir, package_data):
        (project_dir / "package.json").write_text(
            json.dumps(package_data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def run_prepare(self, project_dir, group=None):
        output = io.StringIO()
        args = SimpleNamespace(project_dir=str(project_dir), group=group)
        with contextlib.redirect_stdout(output):
            shadowbot_sync_tool.command_prepare(args)
        return output.getvalue()

    def test_prepare_scans_registers_compiles_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            package_data = {
                "flows": [
                    {
                        "name": "run",
                        "filename": "run",
                        "kind": "Code",
                        "opened": True,
                        "groupName": "主流程",
                        "enableCopilot": True,
                        "customField": "keep",
                    },
                    {
                        "name": "process1",
                        "filename": "process1",
                        "kind": "Visual",
                        "groupName": "可视化",
                    },
                ],
                "flow_groups": [{"name": "主流程"}, {"name": "可视化"}],
            }
            self.write_package_json(project_dir, package_data)
            for file_name in (
                "run.py",
                "low_stock_lock.py",
                "tools.py",
                "process1.py",
                "package.py",
                "__init__.py",
            ):
                (project_dir / file_name).write_text("value = 1\n", encoding="utf-8")

            first_output = self.run_prepare(project_dir)
            first_package_text = (project_dir / "package.json").read_text(encoding="utf-8")
            first_package = json.loads(first_package_text)
            flows = {flow["filename"]: flow for flow in first_package["flows"]}

            self.assertEqual(set(flows), {"run", "process1", "low_stock_lock", "tools"})
            self.assertEqual(flows["run"]["groupName"], "主流程")
            self.assertEqual(flows["run"]["customField"], "keep")
            self.assertFalse(flows["run"]["opened"])
            self.assertFalse(flows["run"]["enableCopilot"])
            self.assertEqual(flows["process1"]["kind"], "Visual")
            self.assertEqual(flows["process1"]["groupName"], "可视化")

            for flow_name in ("low_stock_lock", "tools"):
                self.assertEqual(
                    flows[flow_name],
                    {
                        "name": flow_name,
                        "filename": flow_name,
                        "kind": "Code",
                        "opened": False,
                        "groupName": None,
                        "enableCopilot": False,
                    },
                )

            self.assertNotIn("package", flows)
            self.assertNotIn("__init__", flows)
            for file_name in ("run.py", "low_stock_lock.py", "tools.py", "process1.py"):
                compiled = list(
                    (project_dir / "__pycache__").glob(f"{Path(file_name).stem}.*.pyc")
                )
                self.assertTrue(compiled, file_name)

            self.assertIn("scanned_files=6", first_output)
            self.assertIn("excluded_files=['__init__.py', 'package.py']", first_output)
            self.assertIn("created_flows=['low_stock_lock.py', 'tools.py']", first_output)
            self.assertIn("updated_flows=['run.py']", first_output)
            self.assertIn(
                "compiled_files=['low_stock_lock.py', 'process1.py', 'run.py', 'tools.py']",
                first_output,
            )

            second_output = self.run_prepare(project_dir)
            second_package_text = (project_dir / "package.json").read_text(encoding="utf-8")
            second_package = json.loads(second_package_text)
            filenames = [flow["filename"] for flow in second_package["flows"]]

            self.assertEqual(first_package_text, second_package_text)
            self.assertEqual(len(filenames), len(set(filenames)))
            self.assertIn("created_flows=[]", second_output)

    def test_group_only_applies_to_new_flows(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            self.write_package_json(
                project_dir,
                {
                    "flows": [
                        {
                            "name": "run",
                            "filename": "run",
                            "kind": "Code",
                            "opened": False,
                            "groupName": "主流程",
                            "enableCopilot": False,
                        }
                    ],
                    "flow_groups": [{"name": "主流程"}],
                },
            )
            (project_dir / "run.py").write_text("value = 1\n", encoding="utf-8")
            (project_dir / "constants.py").write_text("VALUE = 1\n", encoding="utf-8")

            self.run_prepare(project_dir, group="工具")
            package_data = json.loads(
                (project_dir / "package.json").read_text(encoding="utf-8")
            )
            flows = {flow["filename"]: flow for flow in package_data["flows"]}

            self.assertEqual(flows["run"]["groupName"], "主流程")
            self.assertEqual(flows["constants"]["groupName"], "工具")
            self.assertIn({"name": "工具"}, package_data["flow_groups"])

    def test_syntax_error_returns_failure_without_saving_flow(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            self.write_package_json(project_dir, {"flows": [], "flow_groups": []})
            original_package_text = (project_dir / "package.json").read_text(encoding="utf-8")
            (project_dir / "broken.py").write_text("def broken(:\n", encoding="utf-8")

            with self.assertRaises(subprocess.CalledProcessError):
                self.run_prepare(project_dir)

            self.assertEqual(
                (project_dir / "package.json").read_text(encoding="utf-8"),
                original_package_text,
            )

    def test_prepare_succeeds_when_only_excluded_files_exist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            self.write_package_json(project_dir, {"flows": [], "flow_groups": []})
            (project_dir / "package.py").write_text("value = 1\n", encoding="utf-8")
            (project_dir / "__init__.py").write_text("value = 1\n", encoding="utf-8")

            output = self.run_prepare(project_dir)

            self.assertIn("scanned_files=2", output)
            self.assertIn("created_flows=[]", output)
            self.assertIn("compiled_files=[]", output)

    def test_prepare_rejects_file_arguments(self):
        parser = shadowbot_sync_tool.build_parser()
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                parser.parse_args(["prepare", "run.py"])


if __name__ == "__main__":
    unittest.main()
