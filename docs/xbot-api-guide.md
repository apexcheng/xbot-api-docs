# 影刀 xbot API 导航指南

本文不是重新复制一套 xbot API，而是帮助开发者和 AI Agent 根据任务快速找到本仓库中正确的影刀编码版文档。

## API 文档入口

完整技术资料位于：

```text
xbot-api-docs/docs/
```

建议先按任务类型选择文档，再查具体对象、参数、返回值和限制。

## 按任务查文档

| 任务 | 文档 | 主要内容 |
| --- | --- | --- |
| 元素库、图像库、资源文件、全局变量 | [`package.md`](../xbot-api-docs/docs/package.md) | 影刀项目基础对象和常用写法 |
| 网页和浏览器操作 | [`browser.md`](../xbot-api-docs/docs/browser.md) | 浏览器对象、元素、点击、输入、下载、Cookie、网络监听 |
| Excel / WPS 自动化 | [`excel.md`](../xbot-api-docs/docs/excel.md) | 工作簿、Sheet、区域、读写和格式 |
| Windows 桌面自动化 | [`win32.md`](../xbot-api-docs/docs/win32.md) | 窗口、桌面对象和 Windows 操作 |
| 键盘和鼠标 | [`keyboard-mouse.md`](../xbot-api-docs/docs/keyboard-mouse.md) | 输入、移动、点击、滚轮和剪贴板 |
| 日志 | [`logging.md`](../xbot-api-docs/docs/logging.md) | 日志输出和导出 |
| 对话框和通知 | [`notification.md`](../xbot-api-docs/docs/notification.md) | 桌面对话框、提示和通知 |
| 压缩与解压 | [`xzip.md`](../xbot-api-docs/docs/xzip.md) | 压缩文件操作 |
| 跨 iframe 操作 | [`iframe2-extension.md`](../xbot-api-docs/docs/iframe2-extension.md) | XPath 查找、点击、输入、等待和信息读取 |
| 市场指令扩展 | [`extension-instructions.md`](../xbot-api-docs/docs/extension-instructions.md) | 扩展目录、参数映射和调用入口 |
| 市场指令源码排查 | [`market-extension-source.md`](../xbot-api-docs/docs/debug/market-extension-source.md) | 编码版异常、参数不明和源码调查 |
| 钉钉 AI 表格 | [`activity-5b77c4ce.md`](../xbot-api-docs/docs/extensions/activity-5b77c4ce.md) | 调用入口、参数、返回结构、数据表、字段、记录、filter、分页和附件 |
| 影刀增强工具 | [`xbot-enhance-tools.md`](../xbot-api-docs/docs/extensions/xbot-enhance-tools.md) | 浏览器等待、下载等待、异常格式化等 |

## 按常见搜索问题定位

### 影刀怎么操作网页？

从 [`browser.md`](../xbot-api-docs/docs/browser.md) 开始。如果页面包含 iframe，再查看 [`iframe2-extension.md`](../xbot-api-docs/docs/iframe2-extension.md)。

### 影刀怎么读取或写入 Excel？

查看 [`excel.md`](../xbot-api-docs/docs/excel.md)，并同时确认实际运行环境使用 Excel 还是 WPS。

### 影刀怎么操作 Windows 窗口？

查看 [`win32.md`](../xbot-api-docs/docs/win32.md)；纯键盘和鼠标动作再配合 [`keyboard-mouse.md`](../xbot-api-docs/docs/keyboard-mouse.md)。

### 影刀编码版怎么使用全局变量？

查看 [`package.md`](../xbot-api-docs/docs/package.md)。

### 影刀市场指令为什么可视化能运行，代码调用却报错？

先查 [`extension-instructions.md`](../xbot-api-docs/docs/extension-instructions.md)，再按 [`market-extension-source.md`](../xbot-api-docs/docs/debug/market-extension-source.md) 的方法确认真实参数结构和调用映射。

### 钉钉 AI 表格怎么读写记录？

先查看 [`activity-5b77c4ce.md`](../xbot-api-docs/docs/extensions/activity-5b77c4ce.md) 的“用法速查”和“典型调用方式”。常用入口是 `xbot_extensions.activity_5b77c4ce.croe.yd_ai_table_action()`，记录列表通常从 `result.get("data", {}).get("records")` 读取。

### 钉钉 AI 表格 filter 怎么写？

查看 [`activity-5b77c4ce.md`](../xbot-api-docs/docs/extensions/activity-5b77c4ce.md) 的“记录筛选 `filter`”。`filter` 是用法问题时优先查结构示例；只有接口返回异常或结果不符合预期时，再按稳定性限制排查。不要因为订单号很长就默认判断为长度问题，应以实际 filter 结构、字段类型和接口返回为依据。

## AI Agent 查 API 的推荐顺序

```text
当前业务任务
    ↓
llms.txt 查入口
    ↓
阅读对应专题文档
    ↓
检查真实项目现有调用
    ↓
检查仓库示例
    ↓
必要时查看市场指令源码
    ↓
在影刀环境验证
```

## 不要混用其他自动化库的经验

影刀 xbot 与以下工具可能解决相似问题，但 API 结构不等同：

- Selenium
- Playwright
- pywin32
- openpyxl
- pandas
- requests

例如，其他库中存在的函数名、参数名、等待方式或返回对象，不代表 xbot 中也可以直接使用。AI Agent 应以本仓库文档和真实项目代码为依据。

## 编写 xbot 代码时的检查点

### 对象来源

确认对象来自哪里：

- 浏览器对象
- 网页元素对象
- Excel / WPS 工作簿对象
- Sheet 或区域对象
- Windows 窗口对象
- 全局变量、元素库或资源文件

### 参数类型

确认参数需要：

- 字符串
- 数字
- 列表
- 字典
- 影刀对象
- 元素库对象
- 路径或 XPath

### 返回值

不要只根据函数名称猜返回值。应确认返回的是：

- 普通值
- 列表或字典
- xbot 对象
- 布尔状态
- 空值
- 异常

### 运行环境

某些行为可能受以下环境影响：

- 影刀版本
- Windows 版本
- Excel 或 WPS
- 浏览器类型
- 登录状态
- 页面结构
- 市场指令版本
- 元素库配置

## 如何记录新的 API 结论

新增或修正文档时，建议包含：

1. 功能说明
2. 最小调用示例
3. 参数解释
4. 返回值
5. 已知限制
6. 错误示例
7. 验证环境
8. 依据来源

未实际运行验证的结论应明确标记，避免 AI Agent 将推测当作稳定规则。

## 相关文档

- [文档中心](README.md)
- [浏览器自动化指南](browser-automation.md)
- [Excel / WPS 自动化指南](excel-automation.md)
- [影刀开发排错指南](troubleshooting.md)
