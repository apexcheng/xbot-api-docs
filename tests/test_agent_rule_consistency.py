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
            "run.py",
            "config.py",
            "tool.py",
            "utils.py",
            "使用位置内联",
            "不因为“有独立业务含义”就拆函数",
            "Service",
            "不增加等价的前置校验",
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

    def test_detailed_examples_remain_available(self):
        root_rules = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        template_rules = (ROOT / "project-template" / "AGENTS.md").read_text(
            encoding="utf-8"
        )
        coding_style = (ROOT / "docs" / "coding-style.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/coding-style.md", root_rules)
        self.assertIn("docs/coding-style.md", template_rules)

        required_details = [
            "采当前页 → 写当前页 → 展示 → 下一页",
            "只使用字典中少数字段",
            "Sphinx / reStructuredText",
            "正常路径直接执行",
            "裸 `raise` 重抛原业务异常",
            "不增加等价的前置校验",
        ]

        for phrase in required_details:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, coding_style)


if __name__ == "__main__":
    unittest.main()
