"""按平台订单号查询 ERP 订单并翻译字段。

运行前提：
- 当前项目已安装 activity_df0688e4
- `args` 提供 platform_order_no
"""

from xbot_extensions.activity_df0688e4 import select_order_dteail, translation


def main(args):
    """查询并返回中文字段的 ERP 订单详情。

    :param args: 影刀流程初始化参数字典
    :type args: dict
    :return: 中文字段订单详情
    :rtype: dict
    """
    platform_order_no = args["platform_order_no"]
    raw_order = select_order_dteail.main({"platform_code": platform_order_no})
    if not raw_order:
        raise RuntimeError(f"未查询到 ERP 订单：{platform_order_no}")
    return translation.main({"record": raw_order}) or {}
