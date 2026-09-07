import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AgentRuleConsistencyTests(unittest.TestCase):
    def test_project_template_keeps_core_agent_constraints(self):
        root_rules = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        template_rules = (ROOT / "project-template" / "AGENTS.md").read_text(
            encoding="utf-8"
        )

        required_phrases = [
            "用户明确给出的 API 调用方式",
            "自上而下的过程式主流程",
            "Service",
            "raise ... from exc",
            "from xbot.app import logging",
            "shadowbot_sync_tool.py",
            "browser.md",
            "win32.md",
            "excel.md",
            "固定 `sleep`",
            "Token",
            "Cookie",
            "Webhook",
            "影刀编辑器",
        ]

        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, root_rules)
                self.assertIn(phrase, template_rules)


if __name__ == "__main__":
    unittest.main()
