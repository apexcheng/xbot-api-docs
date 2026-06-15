"""影刀项目入口骨架。

运行前提：
- 本文件应放在影刀项目代码目录中运行
- 当前项目已具备影刀编码版默认初始化结构
- `args` 中的参数名由人类在影刀编辑器中提前配置
"""

import xbot
from xbot import sleep
from xbot.app import logging

from . import package
from .package import variables as glv


def main(args):
    """影刀项目固定入口。

    :param args: 影刀流程初始化参数字典
    :type args: dict
    """
    shop_name = args.get("shop_name") or ""
    profile = args.get("profile") or "Default"

    logging.info(f"shop_name={shop_name}")
    logging.info(f"profile={profile}")

    glv["shop_name"] = shop_name
    glv["profile"] = profile

    # 这里只是最小入口骨架，真实业务逻辑按项目需要继续补充。
    sleep(1)
