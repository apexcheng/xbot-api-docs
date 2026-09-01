# 影刀日志记录方法

> 定位：影刀 / xbot 编码版的日志输出接口。
> 说明：真实影刀项目里的运行日志优先使用 `xbot.app.logging`；`xbot.print()` 只作为历史兼容写法说明。

---

## 1. 核验来源

本页按 ShadowBot 6.3.12 内置 `xbot/app/logging.py` 与 `xbot/__init__.py` 核对。安装目录随版本变化；其他版本用 `inspect.getfile(xbot.app.logging)` 定位当前实现。

---

## 2. `xbot.app.logging` 与 `xbot.print()`

### 2.1 关系说明

```python
import xbot
from xbot import print as xbot_print
```

- `xbot.app.logging`：提供更细的日志级别控制
- `xbot.print()`：将内容输出到影刀日志面板，内部最终走 `xbot.app.logging.info()`，历史代码可能会用
- Python 内置 `print()`：输出到当前控制台，不会自动进入影刀日志面板

### 2.2 建议

- 当前项目示例和新代码统一使用 `from xbot.app import logging`
- 需要普通运行日志时，用 `logging.info()`
- 需要分级日志时，用 `debug/info/success/warning/error`
- 需要导出日志时，用 `export()`

---

## 3. `trace(*values, sep=' ', end='')`

### 作用

记录 Trace 级日志。

### 常用场景

- 打印调试信息
- 临时查看变量拼接结果
- 输出复杂对象的文本表示

### 参数

| 参数名 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `values` | 任意 | 是 | 一个或多个要打印的对象 |
| `sep` | `str` | 否 | 多个对象之间的分隔符 |
| `end` | `str` | 否 | 结尾字符串 |

### 返回值

无。

### 示例

```python
from xbot.app import logging

logging.trace("page=", 1, ", status=", "ok")
```

### 注意事项

- 会把内容写入日志系统。
- 内部会截断超长内容，避免日志过大。

---

## 4. `debug(text, block=None)`

### 作用

记录 Debug 级日志。

### 常用场景

- 过程调试
- 中间变量输出
- 排查流程分支

### 参数

| 参数名 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `text` | 任意 | 是 | 日志内容 |
| `block` | 任意 | 否 | 传给底层日志接口的附加参数；源码未展开，未确认具体用途 |

### 返回值

无。

### 示例

```python
from xbot.app import logging

logging.debug(f"current_id={current_id}")
```

---

## 5. `info(text, block=None)`

### 作用

记录普通信息日志。

### 常用场景

- 进度提示
- 阶段性结果
- 关键状态输出

### 参数

| 参数名 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `text` | 任意 | 是 | 日志内容 |
| `block` | 任意 | 否 | 传给底层日志接口的附加参数；源码未展开，未确认具体用途 |

### 返回值

无。

### 示例

```python
from xbot.app import logging

logging.info("开始采集")
```

---

## 6. `success(text, block=None)`

### 作用

记录成功日志。

### 常用场景

- 任务完成
- 保存成功
- 校验通过

### 参数

| 参数名 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `text` | 任意 | 是 | 日志内容 |
| `block` | 任意 | 否 | 附加参数；源码未展开，未确认具体用途 |

### 返回值

无。

---

## 7. `warning(text, block=None)`

### 作用

记录警告日志。

### 常用场景

- 数据缺失但不影响主流程
- 需要人工关注但不中断

### 返回值

无。

---

## 8. `error(text, block=None)`

### 作用

记录错误日志。

### 常用场景

- 失败原因记录
- 异常捕获后输出
- 任务终止前留痕

### 返回值

无。

### 示例

```python
from xbot.app import logging

try:
    run_task()
except Exception as e:
    logging.error(f"任务失败：{e}")
    raise
```

---

## 9. `export(save_path)`

### 作用

导出日志到文件。

### 常用场景

- 任务结束后保存日志
- 排查失败现场
- 需要留存运行记录

### 参数

| 参数名 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `save_path` | `str` | 是 | 导出的日志文件路径 |

### 返回值

无。

### 示例

```python
from xbot.app import logging

logging.export(r"C:\logs\run.log")
```

---

## 10. 使用建议

- 运行日志：优先 `info()`。
- 调试细节：用 `debug()` 或 `trace()`。
- 成功/失败状态：用 `success()` / `error()`。
- 需要文件留存：最后调用 `export()`。
- 日志前缀不需要记录时间：影刀日志面板自带时间戳，不要在日志内容里再拼接 `datetime`、`time` 或自定义时间前缀。
