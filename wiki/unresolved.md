# 待验证事项

记录还没有运行验证、源码验证或业务确认的内容。

## 记录格式

```md
## YYYY-MM-DD 待验证标题

- 问题：
- 当前判断：
- 需要验证：
- 验证方式：
- 关联文档：
```

## 记录列表

## 2026-06-13 package 底层对象详细用法

- 问题：`xbot.selector.SelectorStore`、`xbot.selector.ImageSelectorStore`、`xbot.primitives.VariableDict`、`xbot.primitives.ResourceReader` 的底层初始化参数和返回对象行为尚未按当前影刀版本源码验证。
- 当前判断：普通元素定位直接把元素库名称传给 Win32 / Web / Mobile 对应原生 API；`package.image_selector()`、`package.variables`、`package.resources` 按各自公开用途使用，不要在业务代码中直接猜底层对象行为。
- 需要验证：`SelectorStore(name=...)` 的 `name` 与元素库名称的对应关系、`VariableDict()` 是否完整等价于当前项目全局变量、`ResourceReader()` 的资源路径解析规则。
- 验证方式：在真实影刀项目中用 `inspect.signature()`、`inspect.getfile()` 查看当前版本实现，并用最小流程运行确认。
- 关联文档：`xbot-api-docs/docs/package.md`

## 2026-06-13 通知和市场指令参数完整枚举

- 问题：部分参数已能按常见用法开发，但完整枚举仍需源码或运行验证。
- 当前判断：`show_notifycation()` 常见 `placement` / `level` 已在稳定文档记录；`process56`、`qn_login`、`close_ads` 的常见调用已在市场指令文档记录，但完整参数差异不能凭历史项目经验推断。
- 需要验证：`show_notifycation` 的 `placement` / `level` 完整可选值，`process56` 与 `process6` 的全部入参差异，`qn_login.login()` 的 `engine` 完整可选值，`close_ads` 内置广告名单与默认规则。
- 验证方式：按 `xbot-api-docs/docs/debug/market-extension-source.md` 定位当前项目 `xbot_extensions` 源码，查看 `__init__.py`、`_core.py`、`prototype.block.json` 等真实实现。
- 关联文档：`xbot-api-docs/docs/notification.md`、`xbot-api-docs/docs/extension-instructions.md`

## 2026-06-16 iframe2 扩展的 Shadow Root 与运行时边界

- 问题：`iframe2` 已能从源码确认跨 iframe XPath 主能力，但 Shadow Root、隐藏块和不同浏览器下的真实稳定性还没有运行验证。
- 当前判断：`check_obj` 自动包装、XPath 数组逐层切入、`wait` 返回布尔值、`execute_javascript()` 在当前 iframe html 上执行，这些可作为稳定结论；其余运行时边界不应提前泛化。
- 需要验证：Shadow Root 相关路径是否适合当前版本稳定使用，`A2-切换至父IFrame` 隐藏块的可用性，不同浏览器模式下的兼容性，以及页面未完全加载时重试逻辑的实际表现。
- 验证方式：在真实影刀项目里调用 `xbot_extensions.iframe2.api` 的最小示例，分别覆盖单层 iframe、多层 iframe、全局查找、Shadow Root 和加载中页面。
- 关联文档：`xbot-api-docs/docs/iframe2-extension.md`
