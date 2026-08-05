# 影刀 xbot AI Agent 常见问题 FAQ

本文集中回答影刀编码版、xbot API、RPA 自动化、Claude Code、Codex、浏览器自动化和 Excel / WPS 自动化中的常见问题。

## 这个仓库是影刀官方文档吗？

不是。本仓库是面向实际开发和 AI Agent 使用的社区知识库，用于整理 API、规则、示例、排错记录和开发工作流。

## 这个仓库是真实影刀项目吗？

不是。

本仓库负责保存知识、规则和同步工具。真实业务代码应在具体影刀应用的项目目录中修改。

常见真实项目路径类似：

```text
%LOCALAPPDATA%\ShadowBot\users\<user_id>\apps\<app_id>\xbot_robot
```

实际路径应以本机当前应用为准。

## 第一次使用应该先看什么？

建议顺序：

1. [`AGENTS.md`](../AGENTS.md)
2. [`llms.txt`](../llms.txt)
3. [快速开始](getting-started.md)
4. [xbot API 导航指南](xbot-api-guide.md)
5. 当前任务对应的专题文档

## Claude Code 或 Codex 怎么使用这个知识库？

向 Agent 同时提供：

- 本知识库路径
- 真实影刀项目路径
- 业务目标
- 验收标准
- 允许修改范围

然后要求 Agent 先读取 `AGENTS.md` 并检查真实项目现有代码；仅当新增或无法确认 xbot API、市场指令、页面行为时，再按 `llms.txt` 定位相关文档。

详细说明：[AI Agent 开发工作流](ai-agent-development.md)。

## 为什么不能直接让 AI 生成 xbot 代码？

可以生成，但如果没有仓库规则和 API 依据，AI 容易：

- 猜测不存在的方法
- 混用 Selenium、Playwright、openpyxl 等其他库的 API
- 修改错误目录
- 扩大修改范围
- 忽略影刀环境验证

因此推荐先提供项目上下文和本知识库。

## AGENTS.md 和 llms.txt 分别做什么？

- `AGENTS.md`：告诉 Agent 在这个仓库或影刀项目中应遵循什么稳定规则
- `llms.txt`：告诉 Agent 文档在哪里，以及不同问题应读取哪个入口

两者用途不同，建议同时保留。

## 简单修改也需要 TASK.md 吗？

不需要。

`TASK.md` 更适合：

- 新应用
- 多文件修改
- 多阶段任务
- 业务规则复杂
- 存在较多待确认事项

只修改一个函数、参数或错误描述时，可以直接做最小修改。

## 影刀浏览器自动化文档在哪里？

查看：

- [浏览器自动化指南](browser-automation.md)
- [xbot 浏览器 API](../xbot-api-docs/docs/browser.md)
- [iframe2 扩展](../xbot-api-docs/docs/iframe2-extension.md)

## 页面元素找不到怎么办？

优先检查：

- 页面是否正确打开
- 是否需要登录
- 是否出现验证码或风控
- 元素是否在 iframe
- 页面是否尚未加载完成
- 选择器是否依赖随机 class
- 是否返回了不同版本的页面结构

详细说明：[浏览器自动化指南](browser-automation.md)。

## 影刀 Excel / WPS 文档在哪里？

查看：

- [Excel / WPS 自动化指南](excel-automation.md)
- [xbot Excel API](../xbot-api-docs/docs/excel.md)

## 为什么订单号或商品 ID 在 Excel 中变了？

长数字可能被 Excel 当作数值处理，出现科学计数法或精度丢失。开发时应确认该字段是否应该按文本读取和写入。

如果原始文件已经丢失精度，单纯修改显示格式不一定能恢复原值。

## 为什么代码修改后影刀里没有变化？

常见原因：

- 修改的是知识库，不是真实项目目录
- 修改了错误应用目录
- 新增了文件但没有执行同步工具
- 同步目标文件不正确
- 影刀编辑器仍在使用旧内容

请确认真实项目路径；如果新增了文件，再按仓库规则执行 `shadowbot_sync_tool.py`。

## shadowbot_sync_tool.py 在哪里运行？

工具位于本知识库根目录，但 `--project-dir` 应指向真实影刀项目。只有新增文件时才需要执行；仅修改已有文件时不运行。

示例：

```powershell
python "C:\path\to\影刀xAI开发指南\shadowbot_sync_tool.py" ^
  --project-dir "%LOCALAPPDATA%\ShadowBot\users\<user_id>\apps\<app_id>\xbot_robot" ^
  prepare
```

`prepare` 自动扫描该目录下的 Python 文件，不接收文件列表。项目路径必须是包含 `package.json` 的 `xbot_robot` 根目录。

## 市场指令可视化能运行，编码版为什么失败？

可能是：

- UI 参数和代码参数映射不同
- 扩展版本发生变化
- 文档没有暴露真实参数结构
- 请求体层级不同
- 编码版传入类型错误

查看：

- [市场指令扩展开发](../xbot-api-docs/docs/extension-instructions.md)
- [市场指令源码排查](../xbot-api-docs/docs/debug/market-extension-source.md)

## 钉钉 AI 表格 filter 怎么写？

查看 [钉钉 AI 表格文档](../xbot-api-docs/docs/extensions/activity-5b77c4ce.md)。

最小结构示例：

```python
params = {
    "page_size": 1,
    "max_pages": 1,
    "extra_body": {
        "filter": {
            "combination": "and",
            "conditions": [
                {"field": "订单号", "operator": "equal", "value": ["3300000000000000000"]},
            ],
        }
    },
}
```

注意：

1. 顶层参数名使用单数 `filter`，不要写成 `filters`
2. `conditions` 中每个条件的 `value` 必须是列表
3. 只做存在性查询时，优先用 `page_size=1` 和 `max_pages=1`

返回异常或结果不符合预期时，再按下面顺序检查：

1. 无 filter 的查询
2. 单条件 filter
3. 逐个增加条件
4. 更换多个订单号测试
5. 字段类型和 value 类型
6. 请求体层级

不要因为订单号很长就直接判断为长度问题。

## HTTP 500 unknownError 一定是服务端问题吗？

不一定。

500 可能来自服务端异常，也可能由不符合真实要求的请求结构触发。应保留完整响应和 request id，并通过最小请求逐项排除字段、类型和层级问题。

## 为什么固定 sleep 还是不稳定？

因为页面或应用完成时间不是固定的。应优先等待明确条件，例如元素出现、元素可点击、请求完成或文件下载完成，而不是不断增加固定休眠时间。

## 能直接把 Selenium 或 Playwright 代码改成 xbot 吗？

不能机械替换。

它们的对象模型、参数、等待机制和返回值不同。可以参考业务思路，但具体实现必须重新查 xbot 文档并在影刀环境验证。

## 能直接用 openpyxl 的方式操作影刀 Excel 对象吗？

不能默认这样做。

openpyxl 和 xbot Excel / WPS API 是不同体系。除非真实项目明确引入并使用 openpyxl，否则应查 xbot Excel 文档。

## 如何判断一个结论是否可靠？

推荐按证据强度区分：

1. 已在真实影刀环境运行验证
2. 已读取实际扩展源码并确认
3. 有仓库现有稳定代码支持
4. 只有文档描述，尚未实际运行
5. 根据错误现象推测

第 4、5 类应标记为待验证。

## 发现文档写错了怎么办？

不要只覆盖旧结论。建议同时记录：

- 原错误描述
- 正确说法
- 验证依据
- 影响范围

相关入口：

- [错误修正记录](../wiki/error-book.md)
- [待验证事项](../wiki/unresolved.md)

## 如何参与贡献？

适合提交的内容包括：

- 已验证的 xbot API 示例
- 可稳定复现的错误
- 市场指令真实参数说明
- 影刀、Excel / WPS、浏览器环境差异
- 错误文档修正
- 更清晰的教程和索引

提交时应说明验证环境和依据，避免把推测写成确定事实。

## 更多入口

- [文档中心](README.md)
- [快速开始](getting-started.md)
- [AI Agent 开发工作流](ai-agent-development.md)
- [xbot API 导航指南](xbot-api-guide.md)
- [影刀开发排错指南](troubleshooting.md)
