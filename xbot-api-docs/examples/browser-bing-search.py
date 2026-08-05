"""影刀浏览器最小搜索示例。

运行前提：
- 本文件应放在影刀项目代码目录中运行
- 当前环境可直接使用 `xbot.web`
- 页面元素 XPath 需按当前页面实际情况确认
"""

import xbot
from xbot.app import logging

from . import package


def main(args):
    """打开 Bing，输入关键词并点击搜索。

    :param args: 影刀流程初始化参数字典
    :type args: dict
    """
    keyword = args.get("keyword") or "影刀 x Agent驱动开发"

    page = xbot.web.create(url="https://cn.bing.com", mode="chrome", load_timeout=60)
    page.wait_load_completed(timeout=30)

    input_element = page.find_by_xpath("//input[contains(@class, 'sb_form_q')]", timeout=20)
    search_buttons = page.find_all_by_xpath("//input[@name='search']", timeout=20)
    if not search_buttons:
        raise RuntimeError("未找到搜索按钮")

    input_element.input(keyword)
    search_buttons[0].click()

    logging.info(f"已提交搜索关键词: {keyword}")
