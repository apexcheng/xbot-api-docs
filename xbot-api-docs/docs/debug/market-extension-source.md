# 影刀市场指令源码查看方法

> 定位：给 Agent 使用的影刀市场指令调试指南。  
> 重点：当市场指令文档不清楚、可视化能跑但编码版不生效时，先定位 `xbot_extensions`，再查看已安装指令包的实现逻辑。  
> 规则：不要只猜参数，也不要只看包装层签名；真正的参数值、默认值、分支判断，以当前应用中安装的指令源码为准。

---

## 1. 适用场景

遇到下面情况，优先走本文方法：

- 市场指令文档只写了参数名，没写真实取值。
- 可视化流程能运行，但编码版调用不生效。
- 下拉选项不知道应该传中文、英文，还是内部枚举值。
- 指令不报错，但行为和预期不一致。
- 怀疑包装层和底层实现不一致。
- 需要确认指令是否依赖异步线程、JS 注入、页面状态或内部流程。

---

## 2. 核心结论

已安装的市场指令通常会落在当前应用目录的：

```text
xbot_extensions/
```

所以最稳的排查路径是：

```text
确认模块能导入
    ↓
查看包装层函数签名
    ↓
定位模块文件路径
    ↓
进入 xbot_extensions 对应目录
    ↓
查看 _core.py / 其它实现文件
    ↓
确认真实参数值、默认值、分支判断
```

重点：`__init__.py` 很可能只是包装层，不一定是真实逻辑。

---

## 3. 第一步：查看模块和包装层

先确认模块能否导入，以及外层暴露了哪些函数。

```python
import inspect
from xbot_extensions import your_extension_module

print("module:", your_extension_module)
print("file:", inspect.getfile(your_extension_module))
print("dir:", dir(your_extension_module))
```

如果要查看某个函数：

```python
import inspect
from xbot_extensions import your_extension_module

print("signature:", inspect.signature(your_extension_module.some_function))
print("doc:", your_extension_module.some_function.__doc__)
print("source:")
print(inspect.getsource(your_extension_module.some_function))
```

这一步主要确认：

- 外层参数顺序
- 外层参数名
- 是否只是转发到 `xbot_visual.process.run(...)`
- 模块实际安装位置

注意：包装层只能说明“参数怎么传下去”，不一定能说明“底层怎么判断”。

---

## 4. 第二步：定位源码目录

通过 `inspect.getfile(...)` 拿到模块入口文件位置。

```python
import inspect
import os

from xbot_extensions import your_extension_module

base = os.path.dirname(inspect.getfile(your_extension_module))
print("base =", base)
```

常见路径类似：

```text
C:\Users\用户名\AppData\Local\ShadowBot\users\用户ID\apps\应用ID\xbot_extensions\指令包名\
```

重点查看：

```text
__init__.py
_core.py
package.json
其它 .py 文件
配置文件 / 资源文件
```

---

## 5. 第三步：列出目录结构

```python
import inspect
import os

from xbot_extensions import your_extension_module

base = os.path.dirname(inspect.getfile(your_extension_module))
print("base =", base)

for root, dirs, files in os.walk(base):
    level = root.replace(base, "").count(os.sep)
    indent = "  " * level
    print(f"{indent}{os.path.basename(root)}")
    for file_name in files:
        print(f"{indent}  - {file_name}")
```

用这个结果判断真实逻辑在哪个文件里。

常见情况：

| 文件 | 作用 |
|---|---|
| `__init__.py` | 对外入口，很多时候只是包装和转发 |
| `_core.py` | 常见真实实现位置 |
| `package.json` | 指令包配置、参数定义、可视化信息 |
| 其它 `.py` | 具体工具函数、业务逻辑、JS 注入、线程逻辑等 |

---

## 6. 第四步：搜索真实判断逻辑

打开源码后，重点搜索这些内容：

```text
默认值
if xxx == ...
elif xxx == ...
参数名
枚举值
xbot_visual.process.run
thread
javascript
execute_javascript
```

Agent 排查时优先找：

- 参数真实取值
- 默认值
- 布尔参数含义
- 返回值真实结构和异常返回形态
- 中文显示值和内部枚举值的映射
- 是否有异步逻辑
- 是否依赖当前网页对象
- 是否依赖页面刷新前后的状态

---

## 7. 通用排查模板

以后查任何市场指令，可以先用这个模板。

```python
import inspect

from xbot_extensions import your_extension_module

print("module:", your_extension_module)
print("file:", inspect.getfile(your_extension_module))
print("dir:", dir(your_extension_module))

for name in dir(your_extension_module):
    if name.startswith("_"):
        continue

    obj = getattr(your_extension_module, name)
    if not callable(obj):
        continue

    print("\n====", name, "====")

    try:
        print("signature:", inspect.signature(obj))
    except Exception as e:
        print("signature failed:", e)

    try:
        print("doc:", obj.__doc__)
    except Exception as e:
        print("doc failed:", e)

    try:
        print("source:")
        print(inspect.getsource(obj))
    except Exception as e:
        print("getsource failed:", e)
```

---

## 8. Agent 判断规则

Agent 处理市场指令问题时，按下面顺序判断：

### 8.1 先区分包装层和真实实现

如果 `inspect.getsource(...)` 看到的只是参数组装或流程转发，不要直接下结论。

应该继续进入模块目录，查看 `_core.py` 或其它实现文件。

### 8.2 不要把界面显示值当作编码版参数

可视化界面里显示的中文选项，不一定是编码版真实参数。

例如：

```text
界面显示：点击 / 隐藏
编码版可能需要：click / hidden
```

最终以源码里的判断为准。

### 8.3 先确认真实枚举，再修改业务代码

不要反复试：

```python
"点击"
"隐藏"
"click"
"hidden"
```

更稳的做法是直接搜源码里的：

```text
if xxx ==
```

确认后再改业务代码。

### 8.4 不要提交市场指令内部源码

本仓库只记录排查方法、参数结论和调用示例。

不要把第三方市场指令包的完整源码复制进仓库。

### 8.5 返回值结构按指令契约确认

不要预设所有市场指令都返回 `dict`、`list` 或固定对象。封装某个指令前，先通过文档、源码或运行结果确认该指令的返回结构，再决定是否做类型校验、取哪一层字段、失败时如何处理。

例如钉钉 AI 表格指令在已验证项目中按 `dict` 处理，读取多行记录时从 `result.get("data", {}).get("records")` 取列表；这个结论只适用于该指令，不应扩展为“所有市场指令都返回 dict”。

---

## 9. 实战结论示例：广告关闭指令

以广告关闭类市场指令为例，外层函数可能只能看到参数名和顺序，但看不到底层实际枚举值。

排查真实实现后，可以确认：

```text
关闭方式应该传内部枚举值，而不是界面中文显示值。
```

例如编码版调用时，应优先使用源码确认过的值：

```python
from xbot_extensions import ad_killer

ad_killer.close_ads(web_page, "//span[contains(@class, 'close-modal')]", True, "click")
ad_killer.close_ads(web_page, "//span[contains(@class, 'reach-clos')]", False, "click")
```

如果源码里提供了更清晰的底层入口，也可以在确认兼容后直接调用关键函数，并使用关键字参数，让 Agent 更不容易传错：

```python
from xbot_extensions.ad_killer._core import async_close_ads

async_close_ads(
    web_page,
    "//span[contains(@class, 'close-modal')]",
    close_type="click",
    use_builtin=True,
)
```

注意：直接调用 `_core` 这类内部入口前，要确认当前项目是否接受这种写法。更稳的默认做法仍然是使用官方暴露的包装函数。

---

## 10. 一句话给 Agent

遇到影刀市场指令参数不清楚时，不要猜。

先用 `inspect.getfile(...)` 找到当前应用里的 `xbot_extensions` 指令包目录，再查看 `_core.py` 等真实实现文件，确认参数值、默认值和分支判断后再改代码。
