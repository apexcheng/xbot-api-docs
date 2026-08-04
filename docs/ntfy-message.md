# ntfy 消息发送与接收

基于 [ntfy.sh](https://ntfy.sh) 的消息发送与接收模块，支持中文，用于 RPA 场景中 iOS 快捷指令短信内容传递。

## 文件位置

```text
ntfy_message.py
```

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
→ 影刀调用 receive_ntfy_message
→ 获取短信内容
```

## 影刀同步工具

新增 Python 文件后，需运行 `shadowbot_dev_tool.py prepare` 同步：

```bash
python shadowbot_dev_tool.py prepare <文件名.py>
```

工具会自动备份、登记 flow 到 `package.json` 并编译。
