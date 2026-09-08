# 离线 OCR（activity_179ea575）

> 保留的 Python 片段依赖当前流程已取得的对象、输入数据和项目已确认的参数。片段不是独立脚本；[示例边界](../../../AGENTS.md)。

> 调用类型：Visual flow 包装入口
> 证据等级：已从市场指令源码和一个真实项目调用确认；识别效果需在目标图片上运行验证。
> 返回：[市场指令索引](../extension-instructions.md)

---

## 1. 适用场景

识别本地图片或网络图片中的文字。当前未发现等价的原生 `xbot` OCR 接口，因此可保留该市场指令作为 OCR 实现。

## 2. 调用入口

```python
from xbot_extensions import activity_179ea575


ocr_result = activity_179ea575.process1(
    图片路径或图片url=image_path,
    输出完整结果=True,
    文字检测框过滤的阈值=0.4,
    文字检测框的大小=1,
)
```

## 3. 参数说明

| 参数 | 类型 | 示例 | 说明 |
|---|---|---|---|
| `图片路径或图片url` | `str` | `r"C:\Temp\code.png"` | 本地图片路径或网络图片 URL |
| `输出完整结果` | `bool` | `True` | 是否返回包含检测框、文字和置信度等信息的完整结果 |
| `文字检测框过滤的阈值` | `float` | `0.4` | 过滤低置信度检测框的阈值 |
| `文字检测框的大小` | `int` / `float` | `1` | 文字检测框大小相关参数 |

## 4. 最小示例

```text
非执行调用说明（不可直接运行）：

from xbot_extensions import activity_179ea575


result = activity_179ea575.process1(
    图片路径或图片url=r"C:\Temp\ocr.png",
    输出完整结果=False,
    文字检测框过滤的阈值=0.4,
    文字检测框的大小=1,
)
if not result:
    raise RuntimeError("OCR 未识别到文字")
```

## 5. 注意事项

- 本地路径必须在影刀运行机器上真实存在。
- 网络图片能否读取取决于当前网络环境和图片地址权限。
- `输出完整结果=True` 时的具体字段结构以当前市场指令版本返回值为准，使用前先打印或记录一次脱敏结果确认。
- OCR 结果受图片清晰度、缩放、字体、背景和阈值影响，不能仅凭代码调用成功判断识别正确。
