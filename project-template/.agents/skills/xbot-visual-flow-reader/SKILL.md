---
name: xbot-visual-flow-reader
description: Inspect and explain an existing ShadowBot/Yingdao visual orchestration project, especially Visual flows stored as .pybx with related Code flows, selectors, images, and package metadata. Use when a task asks to read, trace, map, or migrate a legacy visual flow; do not trigger for a pure Python-only project.
---

# xbot Visual Flow Reader

读取已有影刀可视化编排项目，输出可追溯的流程地图。本 Skill 默认只读；用户只要求理解或排错时，不修改 `.pybx`、`package.json`、元素库或图像库。

## 先做项目盘点

在真实项目根目录执行：

```powershell
python .agents/skills/xbot-visual-flow-reader/scripts/inspect_visual_project.py .
```

脚本只读取结构元数据，不输出 `package.json` 中的变量值，也不解码 `.pybx`。根据输出确认：

- `startup` 和所有 flow 的 `name` / `filename` / `kind` / `groupName`。
- Visual flow 对应 `.pybx` 是否存在，Code flow 对应 `.py` 是否存在。
- Code flow 的公开函数、参数和 import 关系。
- 全局变量名称、元素库和图像库条目数。

## 证据顺序

1. `package.json`：确认启动流、flow 类型和文件映射。
2. Code flow `.py`：确认 `main(args)`、公开函数、参数与调用边界。
3. `selectorsV2.xml` / `imagesV2.xml` / `package.py`：确认资源名称和对象来源。
4. Visual flow `.pybx`：这是影刀维护的二进制流程文件，不把它当作文本、JSON 或 Python 猜测内部步骤。
5. 需要步骤级逻辑时，使用当前环境可用的影刀 Studio 只读检视能力；先从已安装工具的 help 发现真实命令，不编造命令、标志或流程 ID。

无法打开 Studio 或没有可读导出时，明确写“未确认 Visual flow 内部步骤”，并请用户提供对应流程截图或可读导出；不根据文件名补全业务逻辑。

## 输出要求

将结果分成：

1. **已确认结构**：启动流、Visual / Code flow 列表、实际存在的文件。
2. **已确认调用关系**：有代码、Studio 或可读导出直接证明的调用。
3. **未确认内容**：仅能从名称推测或必须运行才能确认的部分。
4. **修改风险**：启动流、全局变量、元素库、图像库和 Code flow 之间的影响。

不在输出中泄露账号、密码、Token、Cookie、Webhook、客户数据或 `package.json` 变量值。
