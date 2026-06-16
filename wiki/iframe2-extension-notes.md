# iframe2 扩展整理记录

> 资料来源：`xbot_extensions/iframe2/package.json`、`prototype.block.json`、`api.py`、`_core.py`
> 整理日期：2026-06-16

---

## 1. 适用场景

`iframe2` 适合这些开发场景：

- 明确知道目标页面存在一层或多层 `iframe` / `frame`
- 原生元素库不好稳定表达跨 iframe 路径，改用 XPath 更直接
- 编码版里已经拿到 `web_page`，希望继续按 `WebElement` 工作流操作
- 目标业务需要跨 iframe 点击、输入、等待、读取文本或属性

相对更推荐的使用顺序：

1. 先用 `init_iframe()` 或直接传 `web_page`
2. 已知层级时优先传 XPath 数组逐层切入
3. 只有层级不稳定时再考虑 `current_global=True`

---

## 2. 已确认的源码规律

### 2.1 `check_obj` 会自动包装 `web_page`

`api.py` 中除 `init_iframe()` 外的大部分公开方法都挂了 `@check_obj`。

已确认行为：

- 如果传入的 `iframe_instance` 不是 `IframePage`
- `check_obj` 会自动执行 `IframePage(iframe_instance)`
- 所以编码版可以直接把 `web_page` 传给 `find_ele()`、`click_by_xpath()`、`wait()` 等方法

### 2.2 `xpath` 传数组时会逐层切入

`_core.py` 中 `find_ele()` 和 `find_all_ele()` 都先判断：

- `if isinstance(xpath, list):`

已确认行为：

- 前 `n-1` 段按 iframe 路径逐层切入
- 最后一段才作为目标元素 XPath
- 这条路径不依赖 `current_global=True`

### 2.3 `execute_javascript()` 实际跑在当前 iframe html 上

`IframePage.execute_javascript()` 的实现是：

```python
return self.html.execute_javascript(code, argument, execution_world=execution_world)
```

已确认行为：

- 执行对象是当前 `IframePage` 持有的 `html`
- 不是固定回到最外层 `web_page`

---

## 3. 使用边界

### 3.1 全局查找不是默认首选

`current_global=True` 时，底层会遍历当前 iframe 树并尝试在各层查找目标元素。

已确认风险：

- 如果多个 iframe 同时命中，会抛“无法唯一确定”类异常
- 对于结构稳定的页面，这通常不如数组 XPath 可控

建议：

- 切 iframe 时可以酌情打开全局查找
- 找具体业务元素时优先先切准 iframe，再在当前层查

### 3.2 `wait()` 返回布尔值，不返回元素

`wait()` 的职责只是判断出现 / 消失是否满足，结果是 `bool`。

---

## 4. 需运行验证

以下内容目前不建议升格为稳定 API 结论：

- Shadow Root 相关路径在真实业务页面中的可用范围
- 不同浏览器模式下的兼容性差异
- `helpUrl` 指向的官方文档是否仍可用、内容是否和当前源码一致
- 页面未完全加载时，`timeout` 装饰器的重试表现是否和当前推断完全一致
- `A2-切换至父IFrame` 作为隐藏块，在实际项目中的可用性和稳定性

如果后续实测这些边界，建议再同步回稳定文档。

---

## 5. 关联文档

- [iframe2 扩展指令说明](../xbot-api-docs/docs/iframe2-extension.md)
- [市场指令扩展开发](../xbot-api-docs/docs/extension-instructions.md)
- [待验证事项](unresolved.md)
