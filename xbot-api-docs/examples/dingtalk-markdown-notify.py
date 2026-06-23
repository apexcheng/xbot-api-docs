"""钉钉群 Markdown 通知最小示例。

运行前提：
- 本文件应放在影刀项目代码目录中运行
- 当前项目已安装市场指令：钉钉企业机器人消息_v2（dingtalk_bot_message）
- `args` 中的 app_key、app_secret、open_conversation_id 由影刀编辑器提前配置
"""

from xbot.app import logging


def send_markdown_to_group(app_key, app_secret, open_conversation_id, title, content):
    """发送钉钉群 Markdown 消息。

    :param app_key: 钉钉应用 AppKey
    :type app_key: str
    :param app_secret: 钉钉应用 AppSecret
    :type app_secret: str
    :param open_conversation_id: 群会话 ID
    :type open_conversation_id: str
    :param title: 消息标题
    :type title: str
    :param content: Markdown 正文
    :type content: str
    """
    if not (app_key and app_secret and open_conversation_id):
        logging.warning("钉钉群通知参数缺失，已跳过发送。")
        return

    from xbot_extensions.dingtalk_bot_message import process2 as send_group_message

    send_group_message(
        app_key=app_key,
        app_secret=app_secret,
        open_conversation_id=open_conversation_id,
        title=title,
        message_type="markdown",
        content=content,
        webhook_url="",
        webhook_secret="",
        at_mobiles=[],
        at_all=False,
    )


def main(args):
    """发送一条 Markdown 测试通知。

    :param args: 影刀流程初始化参数字典
    :type args: dict
    """
    title = args.get("title") or "影刀任务通知"
    content = args.get("content") or "\n".join([
        "### 影刀任务通知",
        "",
        "- 状态：`完成`",
        "- 说明：这是一条 Markdown 示例消息",
    ])

    send_markdown_to_group(
        app_key=args["app_key"],
        app_secret=args["app_secret"],
        open_conversation_id=args["open_conversation_id"],
        title=title,
        content=content,
    )
    logging.info("钉钉群 Markdown 通知已提交")
