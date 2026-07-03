# 钉钉企业机器人消息_v2 (dingtalk_bot_message)

> 调用类型：`both`  
> 主要入口：通过 __init__.py 的 process1/2/3 调用 flow；to_markdown_table.py 可直接调用。  
> 来源说明：本页由原 extension-instructions.md 的 4.3 节拆出；结论来源见总入口的证据引用。  
> 返回：[市场指令扩展开发指南](../extension-instructions.md)

---

**目录/指令名：** `dingtalk_bot_message` / 钉钉企业机器人消息_v2

**调用方式：** both

**用途：** 发送钉钉私聊消息、群聊消息、生成 markdown 表格

**调用入口：**
- Flow：`xbot_extensions.dingtalk_bot_message.process1(app_key, app_secret, title, message_type, content, user_mobiles)`
- Flow：`xbot_extensions.dingtalk_bot_message.process2(app_key, app_secret, open_conversation_id, title, message_type, content, webhook_url, webhook_secret, at_mobiles, at_all)`
- Direct：`xbot_extensions.dingtalk_bot_message.to_table_format.to_markdown_table(data, max_cell_length)`

**参数说明：**
- `message_type`：消息类型（`text` / `markdown` / `image`）
- `content`：文本/markdown内容 或 图片路径
- `user_mobiles`：接收人手机号列表（私聊，自动换取 userId）
- `webhook_url` / `webhook_secret`：自定义机器人 webhook
- `at_mobiles` / `at_all`：@ 相关

**返回值：** `result`（发送结果）

**注意事项：**
- 群聊图片需要 `app_key` + `app_secret` + `open_conversation_id`
- 群聊文本/Markdown 可以用 webhook 机器人
- `to_table_format.py` 可直接调用生成 markdown 表格

**典型调用方式：**
```python
# 发送私聊消息
xbot_extensions.dingtalk_bot_message.process1(
    app_key="xxx", app_secret="xxx",
    title="通知", message_type="markdown",
    content="## 标题\n内容", user_mobiles=["13800138000"]
)

# 生成 markdown 表格
from xbot_extensions.dingtalk_bot_message.to_table_format import to_markdown_table
md = to_markdown_table(
    data=[["a", "b"], ["1", "2"]],
    max_cell_length=100
)
```

**项目里的 Markdown 群通知模式：**

```python
from xbot_extensions.dingtalk_bot_message import process2 as send_group_message
from xbot.app import logging

try:
    send_group_message(
        app_key=app_key,
        app_secret=app_secret,
        open_conversation_id=open_conversation_id,
        title="商品链接价格监测完成",
        message_type="markdown",
        content=content,
        webhook_url="",
        webhook_secret="",
        at_mobiles=[],
        at_all=False,
    )
except Exception as e:
    logging.error(f"钉钉群通知发送失败：{e}")
```

补充约定：

- 群通知里更推荐 `title` 和 `content` 分离，正文统一传 Markdown。
- 如果通知失败只影响提醒链路，不影响主业务，可只记录日志，不中断主流程。

---
