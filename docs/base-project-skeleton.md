# 影刀编码版最小 base 骨架

本骨架用于新建或补全真实影刀 xbot 编码版项目。它依据维护者提供的真实项目于 2026-09-01 核验，不记录本机用户 ID、应用 ID 和业务凭据。

## 经过核验的结构

参考项目的 `package.json` 包含三个流程：

```text
main     Visual   项目启动流
run      Code     编码版业务入口
config   Code     配置路径
```

`startup` 指向 `main`。`main.pybx`、`package.json`、`package.py`、`selectorsV2.xml` 和 `imagesV2.xml` 由影刀维护，不从知识库模板覆盖。

## 需要复制的文件

将 `project-template/` 中的文件复制到已存在 `package.json` 的真实项目根目录。其中的 base 代码是：

- `run.py`：通过 `main(args)` 进入业务，首次运行显示配置对话框。
- `config.py`：保存当前 Windows 用户下的加密配置文件路径。
- `shadowbot_sync_tool.py`：登记和编译新增 Code 流。

`run.py` 依赖项目已安装“增强工具2026”市场指令，使用其公开 `market_config` 能力：

```text
load_secret_config()
→ 无配置时 show_custom_dialog()
→ dialog_result_to_dict()
→ 用户选择保存时 save_secret_config()
→ 进入业务流程
```

加密配置使用 Windows DPAPI，与当前 Windows 用户绑定，不是跨用户、跨机器配置。详细 API 事实见 [增强工具2026](../xbot-api-docs/docs/extensions/xbot-enhance-tools.md)。

## Agent 实现规则

1. 影刀 Code 流入口使用 `main(args)`；`args` 是流程初始化参数字典，不等于 `package.variables`。
2. 已知入参名时严格使用已有名称；不同时兼容多个猜测名称。
3. 输入形态不确定时，只在 `main(args)` 边界归一化一次。
4. 修改 `dialog_settings` 时，`VariableName` 是转换后的配置字段名，按钮结果从 `pressed_button` 读取。
5. 不在代码、模板、日志或 Git 中保存明文账号、密码、Token 或 Webhook。
6. 新增 `.py` 文件后，在项目根目录直接执行 `python shadowbot_sync_tool.py`，不向脚本传文件列表。

## 最小验收

1. `package.json` 仍由影刀维护，同步前保留备份。
2. `python shadowbot_sync_tool.py` 成功登记 `run.py` 和 `config.py`。
3. 首次运行显示初始化对话框，取消时流程正常结束。
4. 保存后再次运行能加载配置；不把同步成功表述成已在影刀中运行验证。
