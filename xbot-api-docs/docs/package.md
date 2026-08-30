# 影刀基础对象与全局变量

> 定位：影刀 RPA Python 编码版里的 `package` 运行时辅助对象。
> 说明：以下内容结合官方接口文档笔记整理，当前仓库未直接提取到 `package` 源码实现；若客户端版本不一致，以影刀客户端内置提示或官方文档为准。

---

## 1. 作用

`package` 主要用于访问当前应用中的：

- 图像库选择器
- 资源文件
- 全局变量

常见写法：

```python
from . import package
```

---

## 2. `package.image_selector(name)`

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

## 3. `package.resources`

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

## 4. `package.variables`

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

## 5. 组合用法

### 5.1 元素库 + 全局变量

```python
from . import package

web_page = package.variables["web_page"]

web_page.wait_load_completed(timeout=30)
query_btn = web_page.find("按钮_查询", timeout=10)
query_btn.click()
```

### 5.2 资源文件 + 全局变量

```python
from . import package

template_file = package.resources.get_path("模板.xlsx")
package.variables["template_file"] = template_file
```

### 5.3 凭证变量 + 市场指令

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

## 6. 经验

- `package.resources` 只用于访问随应用打包的固定资源，不适合保存运行时动态生成内容。
- 当前可见 `ResourceReader` 公开方法是 `get_path()`、`get_text()`、`get_bytes()`、`copy_to()`、`copy_to_clipboard()`；不要把 `package.resources` 当字典使用，也不要写 `package.resources["模板.xlsx"]`。
- 需要从模板补齐缺失 Excel 文件时，优先用 `package.resources.get_path()` 获取模板路径，或用 `package.resources.copy_to()` 复制模板到目标路径。
- 同一轮任务中，多个记录共享同一页面、SPU、接口响应或解析结果时，可以用 `package.variables` 保存任务级缓存，减少重复打开页面和重复解析。
- 任务开始时应显式初始化或清空任务级缓存，避免跨轮任务误用旧数据。
- 缓存内容只放本轮可复用的中间结果，不要存账号密码、token、Cookie 等敏感数据。
- Agent 写代码时，优先复用项目里已有元素名、资源名、变量名；不要凭感觉新造名字。

---

## 7. 低频：显式获取 `Selector` 对象

普通 Win32 / Web / Mobile 元素定位直接把元素库名称传给对应原生 API，不需要显式获取 `Selector` 对象。

只有确实需要读取或处理选择器对象本身的元数据时，才使用 `package.selector()`：

```python
from . import package

selector = package.selector("目标元素")
framework = selector.framework()
xpath = selector.xpath()
```

---

## 8. 快速建议

- 需要引用图片时，用 `package.image_selector()`。
- 需要跨流程传对象时，用 `package.variables`。
- 需要随应用打包的文件时，用 `package.resources`。
- Agent 写代码时，优先复用项目里已经定义好的元素名、资源名、变量名，不要擅自发明一套新命名。
