# 增强工具2026：ntfy 消息发送与接收

基于 [ntfy.sh](https://ntfy.sh) 的消息发送与接收功能，支持中文，用于 RPA 场景中 iOS 快捷指令与影刀之间传递短信内容。

该功能不是新增在某个普通影刀应用中的独立工具文件，而是新增在市场指令 **“增强工具2026”** 的源码项目中。

## 文件位置

```text
C:\Users\Administrator\AppData\Local\ShadowBot\users\859019956984664066\apps\8f2c6521-41ea-4654-8f7d-b36acd08b892\xbot_robot\ntfy_message.py
```

市场指令信息：

- 名称：`增强工具2026`
- 项目 UUID：`8f2c6521-41ea-4654-8f7d-b36acd08b892`
- 扩展代码：`xbot_enhance_tools`
- 模块路径：`xbot_extensions.xbot_enhance_tools.ntfy_message`

## 依赖

`requests`（已在影刀项目中安装）

## 方法

### send_ntfy_message

```python
def send_ntfy_message(message, topic, server="https://ntfy.sh")
```

HTTP POST 发送纯文本消息到指定 topic。

- `message`: 消息内容，支持中文
- `topic`: ntfy topic 名称
- `server`: ntfy 服务器地址，默认 `https://ntfy.sh`

返回 `True`，失败时抛出异常。

### receive_ntfy_message

```python
def receive_ntfy_message(topic, server="https://ntfy.sh", since="10m", timeout=15)
```

轮询拉取指定 topic 的消息（流式 SSE，实时解析）。

- `topic`: ntfy topic 名称
- `server`: ntfy 服务器地址，默认 `https://ntfy.sh`
- `since`: 拉取时间范围，默认 `10m`（10分钟）
- `timeout`: 请求超时（秒），默认 15

返回 `{"id": "...", "time": ..., "message": "..."}` 或 `None`（无消息时）。

## 使用链路

```
iOS 快捷指令 → ntfy topic
→ 影刀通过“增强工具2026”调用 receive_ntfy_message
→ 获取短信内容
```

## 开发与同步说明

`ntfy_message.py` 属于“增强工具2026”市场指令源码。修改功能时，应直接在上述市场指令项目中开发和同步，不要把该文件复制到普通影刀应用，也不要在普通应用中运行 `shadowbot_dev_tool.py prepare <文件名.py>`。

当前项目已经在 `package.json`、`__init__.py` 和市场指令原型文件中登记 `ntfy_message`。后续修改现有功能时，只需维护该市场指令项目中的源码，并按“增强工具2026”的正常发布流程更新市场指令。
