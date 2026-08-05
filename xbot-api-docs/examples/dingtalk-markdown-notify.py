"""通过 Webhook 发送钉钉群 Markdown 通知。

运行前提：
- 本文件应放在影刀项目代码目录中运行
- 当前项目已安装市场指令：钉钉企业机器人消息_v2（dingtalk_bot_message）
- `args` 中的 webhook_url 由影刀编辑器提前配置
- 自定义机器人启用了加签时，同时配置 webhook_secret
"""

from xbot.app import logging
from xbot_extensions.dingtalk_bot_message.py_api import send_dingtalk_group


def main(args):
    """发送一条 Markdown 测试通知。

    :param args: 影刀流程初始化参数字典
    :type args: dict
    :return: 钉钉接口返回结果
    """
    webhook_url = args["webhook_url"]
    webhook_secret = args.get("webhook_secret") or None
    title = args.get("title") or "影刀任务通知"
    content = args.get("content") or "\n".join([
        "### 影刀任务通知",
        "",
        "- 状态：`完成`",
        "- 说明：这是一条 Markdown 示例消息",
    ])

    try:
        result = send_dingtalk_group("markdown", content, webhook_url=webhook_url, webhook_secret=webhook_secret, title=title)
    except Exception as error:
        logging.error(f"钉钉群通知发送失败：{error}")
        raise

    logging.info("钉钉群 Markdown 通知发送成功")
    return result
