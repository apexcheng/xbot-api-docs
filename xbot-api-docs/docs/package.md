# 影刀基础对象与全局变量

> 定位：影刀 RPA Python 编码版里的 `package` 运行时辅助对象。
> 说明：以下内容结合官方接口文档笔记整理，当前仓库未直接提取到 `package` 源码实现；若客户端版本不一致，以影刀客户端内置提示或官方文档为准。

---

## 1. 作用

`package` 主要用于访问当前应用中的：

- 元素库选择器
- 图像库选择器
- 资源文件
- 全局变量

常见写法：

```python
from . import package
```

---

## 2. `package.selector(name)`

### 作用

按“元素库里保存的名称”获取元素选择器。

### 常用场景

- 点击页面按钮
- 输入框定位
- 软件窗口控件定位
- 列表/表格元素定位

### 示例

```python
from . import package

query_btn = package.selector("按钮_查询")
query_btn.click()
```

### Agent 常见写法

```python
from . import package

search_input = package.selector("输入框_关键词")
search_button = package.selector("按钮_搜索")

search_input.input("影刀")
search_button.click()
```

### 注意事项

- 传入的是元素库名称，不是页面文本。
- 如果名称写错，会直接找不到选择器。
- 不要把网页中看到的文字当成元素库名称。
- 优先把稳定元素维护到元素库，再通过 `package.selector()` 取，不要在代码里到处硬写同一套选择器。

---

## 3. `package.image_selector(name)`

### 作用

按图像库名称获取图像选择器。

### 常用场景

- 等待图像出现
- 点击图像
- 校验图像是否存在

### 示例

```python
from . import package

logo = package.image_selector("登录成功标志")
```

### Agent 常见场景

```python
from . import package

captcha_image = package.image_selector("验证码区域")
success_logo = package.image_selector("登录成功标记")
```

### 注意事项

- 通常配合 `xbot.win32.Image` 使用。
- 图像选择器的稳定性依赖截图质量和页面状态。
- 图像选择器更适合兜底，不要优先替代能稳定定位的网页元素。

---

## 4. `package.resources`

### 作用

访问应用资源文件。

当前知识库按本机可见源码 `C:\Program Files\ShadowBot\shadowbot-6.0.30\Resources\Code-Activity\Zh-CN\xbot\primitives.py` 中的 `ResourceReader` 公开方法整理；这里只记录当前可见方法，不额外推断未确认行为。

### 常用场景

- 读取模板 Excel
- 读取配置文件
- 读取图片或临时数据文件

### 当前可见方法

- `get_path(filename) -> str`：获取资源文件路径
- `get_text(filename, encoding='utf-8') -> str`：读取资源文件文本内容
- `get_bytes(filename) -> bytes`：读取资源文件二进制内容
- `copy_to(filename, dest_filename)`：复制资源文件到指定路径
- `copy_to_clipboard(filenames)`：将资源文件加入剪贴板

### `get_path()`

```python
from . import package

file_path = package.resources.get_path("模板.xlsx")
```

### `get_text()`

```python
from . import package

config_text = package.resources.get_text("config.json")
```

### `get_bytes()`

```python
from . import package

logo_bytes = package.resources.get_bytes("logo.png")
```

### `copy_to()`

```python
from . import package

package.resources.copy_to("模板.xlsx", r"D:\temp\模板.xlsx")
```

### `copy_to_clipboard()`

```python
from . import package

package.resources.copy_to_clipboard(["模板.xlsx", "logo.png"])
```

### 典型场景

- Excel 模板路径传给 `xbot.excel.open()`
- 配置文件文本内容传给 JSON / 文本读取逻辑
- 图片二进制内容或路径传给上传、比对或通知逻辑

### 注意事项

- `package.resources` 更适合读“跟项目一起打包”的固定文件，不适合存运行时动态生成内容。
- 当前知识库以本机可见 `ResourceReader` 方法为准，`package.resources["xxx"]` 不应再作为可用写法保留。
- 当前可见源码没有确认 `package.resources` 支持下标访问，不要把它当成字典使用。
- 若运行结果与当前版本不一致，标注“需运行验证”。

---

## 5. `package.variables`

### 作用

读写影刀应用运行时的全局变量。

### 常用场景

- 保存浏览器对象
- 保存账号、店铺、任务状态
- 在多个流程间传递数据
- 存储密钥、凭证等敏感配置

### 示例

```python
from . import package

package.variables["web_page"] = browser
web_page = package.variables["web_page"]
```

### Agent 最常见用法

#### 1. 保存网页对象供后续流程继续使用

```python
from . import package

package.variables["web_page"] = browser
web_page = package.variables["web_page"]
```

#### 2. 读取账号、店铺、时间范围等运行参数

```python
from . import package

shop_name = package.variables["shop_name"]
start_date = package.variables["start_date"]
end_date = package.variables["end_date"]
```

#### 3. 读取接口凭证或配置

```python
from . import package

app_key = package.variables["APP_KEY"]
session_key = package.variables["SESSION_KEY"]
secret = package.variables["SECRET"]
```

#### 4. 回写流程结果

```python
from . import package

package.variables["collect_status"] = "success"
package.variables["collect_count"] = 20
```

### 注意事项

- 使用前要在影刀编辑器中先创建对应变量名。
- 脚本结束后变量通常不会长期保留。
- 敏感信息优先放到全局变量，不建议硬编码。
- 读变量前，先确认变量名是否由当前项目约定好，不要凭感觉新造名字。
- 浏览器对象、列表、字典等运行时对象可以放进去，但前提是后续流程确实会继续消费这些对象。

---

## 6. 组合用法

### 6.1 元素库 + 全局变量

```python
from . import package

web_page = package.variables["web_page"]
query_btn = package.selector("按钮_查询")

web_page.wait_load_completed(timeout=30)
query_btn.click()
```

### 6.2 资源文件 + 全局变量

```python
from . import package

template_file = package.resources.get_path("模板.xlsx")
package.variables["template_file"] = template_file
```

### 6.3 凭证变量 + 市场指令

```python
from . import package
from xbot_extensions.guanyi_erp_api.core import build_payload, gy_call

payload = build_payload(
    method="gy.erp.stock.get",
    app_key=package.variables["APP_KEY"],
    session_key=package.variables["SESSION_KEY"],
    secret=package.variables["SECRET"],
)
result = gy_call(payload)
```

## 7. 快速建议

- 需要引用元素时，用 `package.selector()`。
- 需要引用图片时，用 `package.image_selector()`。
- 需要跨流程传对象时，用 `package.variables`。
- 需要随应用打包的文件时，用 `package.resources`。
- Agent 写代码时，优先复用项目里已经定义好的元素名、资源名、变量名，不要擅自发明一套新命名。
