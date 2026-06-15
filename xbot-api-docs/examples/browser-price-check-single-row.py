"""浏览器抓价并回写钉钉 AI 表格的单行示例。

运行前提：
- 本文件应放在影刀项目代码目录中运行
- 当前环境可直接使用 `xbot.web`
- 当前项目已安装市场指令：钉钉AI表格（activity_5b77c4ce）
- `args` 中的 client_id、client_secret、base_id、user_id 由影刀编辑器提前配置
- 表格中存在 `商品链接价格监测` 工作表，并包含 `链接`、`目标价格`、`实际价格`、`巡检状态`、`更新时间` 字段
- 示例 XPath 需按当前页面实际情况确认
"""

import re
from datetime import datetime

from xbot import web
from xbot.app import logging


def table_action(action, client_id, client_secret, base_id, user_id, sheet, params=None):
    """调用钉钉 AI 表格指令。

    :param action: 操作名称
    :type action: str
    :param client_id: 钉钉应用 AppKey
    :type client_id: str
    :param client_secret: 钉钉应用 AppSecret
    :type client_secret: str
    :param base_id: AI 表格 baseId
    :type base_id: str
    :param user_id: 操作人 userId
    :type user_id: str
    :param sheet: 工作表名称
    :type sheet: str
    :param params: 指令参数
    :type params: dict | None
    :return: 指令返回结果
    :rtype: dict
    """
    from xbot_extensions.activity_5b77c4ce.croe import yd_ai_table_action

    result = yd_ai_table_action(
        action=action,
        client_id=client_id,
        client_secret=client_secret,
        base_id=base_id,
        user_id=user_id,
        sheet=sheet,
        params=params or {},
    )
    if not isinstance(result, dict):
        raise ValueError(f"表格操作 {action} 返回异常: {result!r}")
    return result


def parse_price(text):
    """从页面文本中提取价格数字。

    :param text: 页面价格文本
    :type text: str
    :return: 价格数字，无法提取时返回 None
    :rtype: float | None
    """
    match = re.search(r"-?\d+(?:\.\d+)?", str(text or ""))
    return float(match.group(0)) if match else None


def main(args):
    """读取第一条商品记录，打开链接抓价，并回写实际价格。

    :param args: 影刀流程初始化参数字典
    :type args: dict
    """
    client_id = args["client_id"]
    client_secret = args["client_secret"]
    base_id = args["base_id"]
    user_id = args["user_id"]
    sheet = args.get("sheet") or "商品链接价格监测"
    price_xpath = args.get("price_xpath") or "//span[contains(@class, 'price')]"

    result = table_action(
        "获取多行记录分页",
        client_id,
        client_secret,
        base_id,
        user_id,
        sheet=sheet,
        params={"page_size": 1, "max_pages": 1},
    )
    records = result.get("data", {}).get("records") or []
    if not records:
        raise ValueError(f"表格「{sheet}」无数据")

    record = records[0]
    fields = record["fields"]
    record_id = record.get("id") or record.get("recordId") or record.get("record_id")
    link = str(fields.get("链接") or "").strip()
    if not record_id:
        raise ValueError("记录缺少 ID")
    if not link:
        raise ValueError("记录缺少链接")

    browser = web.create(url=link, mode="chrome", load_timeout=30)
    browser.wait_load_completed(timeout=20)

    price_text = browser.find_by_xpath(price_xpath, timeout=20).get_text()
    actual_price = parse_price(price_text)
    if actual_price is None:
        actual_value = "获取失败"
        status = "价格获取失败"
    else:
        actual_value = actual_price
        target_price = fields.get("目标价格")
        status = "已获取价格" if target_price in (None, "") else ("价格一致" if abs(actual_price - float(target_price)) < 1e-6 else "价格不一致")

    table_action(
        "更新多行记录",
        client_id,
        client_secret,
        base_id,
        user_id,
        sheet=sheet,
        params={"records": [{"id": record_id, "fields": {"实际价格": actual_value, "巡检状态": status, "更新时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}]},
    )
    logging.info(f"已回写实际价格: {actual_value}，状态: {status}")
