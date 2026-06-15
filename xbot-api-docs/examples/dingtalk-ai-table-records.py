"""钉钉 AI 表格最小读写示例。

运行前提：
- 本文件应放在影刀项目代码目录中运行
- 当前项目已安装市场指令：钉钉AI表格（activity_5b77c4ce）
- `args` 中的 client_id、client_secret、base_id、user_id 由影刀编辑器提前配置
- 表格中存在 `商品链接价格监测` 工作表，并包含 `平台`、`目标价格`、`实际价格` 字段
"""

from xbot.app import logging


def table_action(action, client_id, client_secret, base_id, user_id, sheet, params=None):
    """调用钉钉 AI 表格指令。

    :param action: 操作名称，如 获取多行记录分页、更新多行记录
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


def main(args):
    """读取前 10 条记录，并把第一条记录的实际价格回写为示例值。

    :param args: 影刀流程初始化参数字典
    :type args: dict
    """
    client_id = args["client_id"]
    client_secret = args["client_secret"]
    base_id = args["base_id"]
    user_id = args["user_id"]
    sheet = args.get("sheet") or "商品链接价格监测"

    result = table_action(
        "获取多行记录分页",
        client_id,
        client_secret,
        base_id,
        user_id,
        sheet=sheet,
        params={"page_size": 10, "max_pages": 1},
    )
    records = result.get("data", {}).get("records") or []
    logging.info(f"读取到 {len(records)} 条记录")
    if not records:
        return

    first_record = records[0]
    fields = first_record["fields"]
    logging.info(f"第一条记录平台: {(fields.get('平台') or {}).get('name') or fields.get('平台') or ''}")

    record_id = first_record.get("id") or first_record.get("recordId") or first_record.get("record_id")
    if not record_id:
        raise ValueError("第一条记录缺少记录 ID")

    table_action(
        "更新多行记录",
        client_id,
        client_secret,
        base_id,
        user_id,
        sheet=sheet,
        params={"records": [{"id": record_id, "fields": {"实际价格": "示例回写"}}]},
    )
    logging.info("已回写第一条记录的实际价格字段")
