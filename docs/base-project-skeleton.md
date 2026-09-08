# 影刀编码版最小 base 骨架

本骨架用于新建或补全真实影刀 xbot 编码版项目。流程结构和配置 API 依据维护者提供的真实项目于 2026-09-01 核验；项目内配置路径的运行验证边界见下文。不记录本机用户 ID、应用 ID 和业务凭据。

## 经过核验的结构

参考项目的 `package.json` 包含三个流程：

```text
main     Visual   项目启动流
run      Code     编码版业务入口
config   Code     配置路径
```

`startup` 指向 `main`。`main.pybx`、`package.json`、`package.py`、`selectorsV2.xml` 和 `imagesV2.xml` 由影刀维护，不从知识库模板覆盖。

## 需要复制的文件

将 `project-template/` 中缺失的文件复制到已存在 `package.json` 的真实项目根目录。目标已有同名文件时，先保留原文件和用户改动，再按当前需求最小合并；不得整份覆盖已有 `run.py`、`config.py`、`.gitignore` 或规则文件。其中的 base 代码是：

- `run.py`：通过 `main(args)` 进入业务，首次运行显示配置对话框。
- `config.py`：保存当前项目 `.dev/project_config.json` 的加密配置路径。
- `shadowbot_sync_tool.py`：登记和编译新增 Code 流。

`run.py` 依赖项目已安装“增强工具2026”市场指令，使用其公开 `market_config` 能力：

```text
load_secret_config()
→ 无配置时 show_custom_dialog()
→ dialog_result_to_dict()
→ 用户选择保存时 save_secret_config()
→ 进入业务流程
```

模板按 `config.py` 所在目录定位 `.dev/project_config.json`，各项目使用自己的配置文件。模板不读取、迁移或回退到旧的用户目录 `.xbot/project_config.json`；新位置没有配置时，沿用初始化流程，旧文件保持不变。需要迁移时先由项目维护者确认旧配置归属。

`.dev/` 已被项目模板的 `.gitignore` 忽略，但 Git 忽略不代表影刀发布时自动排除。加密仍使用与当前 Windows 用户绑定的 DPAPI，更换用户或机器后不能直接复用配置。详细 API 事实见 [增强工具2026](../xbot-api-docs/docs/extensions/xbot-enhance-tools.md)。

**需运行验证：**影刀 Code 流运行时 `__file__` 的实际位置，以及 `.dev` 是否进入影刀打包或发布。若 `config.py` 不位于真实项目根目录，配置路径验收不通过，不回退共享路径或猜测其他目录。普通 Python 路径测试和 Git 忽略规则不能证明这些运行行为。

## Agent 实现规则

入口、参数、敏感信息与同步遵守[根开发规则](../AGENTS.md)。本模板只补充以下约定：

- `args` 是流程初始化参数字典，不等于 `package.variables`。
- 修改 `dialog_settings` 时，`VariableName` 是转换后的配置字段名，按钮结果从 `pressed_button` 读取。

## 最小验收

1. 仅新增缺失文件；已有入口、配置与用户改动保留。按根规则需要同步时，先备份 `package.json`，再确认新增 Code 流已登记；用户要求暂不同步时记录未执行。
2. 在影刀 Code 流中确认配置实际位于当前项目 `.dev/project_config.json`，并核查 `.dev` 的打包、发布边界。
3. 首次运行显示初始化对话框，取消时流程正常结束；保存后再次运行能加载本项目配置。
4. 同一 Windows 用户下两个项目互不串用配置，旧共享文件不被读取、覆盖或迁移。
5. 未具备真实影刀验收条件时，将上述运行项明确保留为“需运行验证”，不把同步或静态检查视为运行通过。
