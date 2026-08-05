"""初始化 C-ERP 并下载发货订单明细。

运行前提：
- 当前项目已安装 C-ERP 市场指令（activity_a90a8311）
- `args` 提供 username、password、start_date、end_date
"""

from xbot_extensions import activity_a90a8311


def main(args):
    """下载指定日期范围的发货订单明细。

    :param args: 影刀流程初始化参数字典
    :type args: dict
    :return: 下载文件路径
    :rtype: str
    """
    activity_a90a8311.process13(username=args["username"], password=args["password"], ERP浏览器标识=args.get("profile") or "Default", refresh=True)
    file_path = activity_a90a8311.process14(店铺名称=args.get("shop_name"), 发货时间start=args["start_date"], 发货时间end=args["end_date"])
    if not file_path:
        raise RuntimeError("发货订单明细下载未返回文件路径")
    return file_path
