# Excel 与表格处理经验

本文沉淀影刀项目中 Excel、WPS 和表格数据处理的跨项目经验，不替代 `xbot-api-docs/docs/excel.md` 的 API 参数说明。

## 1. 字符串参数按文档原样传入

- `kind` 等字符串参数大小写敏感，按文档传 `kind="wps"`、`kind="office"`、`kind="openpyxl"`。
- 不要写 `kind="WPS"`、`kind="PWS"`、`kind="Office"` 这类界面化或猜测值。
- 可视化界面能跑，不代表编码版参数也能传中文或展示值；编码版以文档或源码为准。

## 2. 按场景选择 Excel 能力

- 影刀项目默认优先使用 `xbot.excel` 对应能力处理 Excel / WPS 文件。
- 涉及公式刷新、界面交互、宏、另存、格式、文件占用、真实 Office / WPS 行为时，必须按 `xbot.excel` 文档开发。
- 不要为了图快改用其它后台读写库，除非用户明确要求且当前任务不依赖真实 Excel / WPS 行为。

## 3. 大量写入优先二维数组

- 表格大量写入时，优先整理成二维数组后批量写入，减少逐单元格操作。
- 写入前先明确表头、起始单元格和目标区域，避免边写边推断字段。
- 如果需要保留公式或格式，先确认批量写入是否会覆盖目标区域已有内容。

## 4. 写入前必须二次判断工作簿只读状态

- 需要写入 Excel / WPS 表格时，必须使用 `workbook.workbook.ReadOnly` 判断工作簿是否为只读。
- 这条经验适用于 `kind="wps"` / `kind="office"` 这类真实 Excel / WPS 工作簿对象，不扩展到 `kind="openpyxl"`。
- 第一次 `ReadOnly=True` 不一定代表文件被他人占用，也可能是本机残留的 Excel / WPS 进程占用导致。
- 正确流程：先打开文件并判断 `ReadOnly`；如果为 `True`，先 kill 本机 WPS / Excel 进程，再重新打开文件并二次判断；只有第二次仍为 `True`，才判定文件被他人占用，并 `raise` 异常停止写入。

```python
workbook = xbot.excel.open(
    file_name=file_path,
    kind="wps",
    visible=True,
    password="",
    write_password="",
    ignore_formula=True,
    update_links=False,
)

if workbook.workbook.ReadOnly:
    workbook.close()
    xbot.excel.kill_excel_process("wps", True)

    workbook = xbot.excel.open(
        file_name=file_path,
        kind="wps",
        visible=True,
        password="",
        write_password="",
        ignore_formula=True,
        update_links=False,
    )
    if workbook.workbook.ReadOnly:
        workbook.close()
        raise ValueError("当前表格仍为只读，可能已被他人占用，停止写入")
```

- 如果项目使用 `kind="office"`，对应关闭进程时使用 `xbot.excel.kill_excel_process("office", True)`。

## 5. 表格字段和业务字段边界

- 字段名来自当前业务表时，不要抽成跨项目通用常量。
- 当前项目已约定字段结构时，业务逻辑直接按约定取值，不要反复写 `isinstance` 和空结构兜底。
- 字段结构不确定时，只在入口边界统一归一化一次；确认不了就标注“需运行验证”。

## 6. 可视化写入过程偏好

- 用户需要看到 WPS / Excel 写入过程时，打开表格后用当前文件名通配符匹配窗口，激活并最大化窗口。
- 每次写入数据前先激活表格窗口，写入后选中本次新增行号，方便用户确认数据正在持续写入。
- 找窗口优先使用 `xbot.win32.get(title="*文件名*", use_wildcard=True)`，不要优先坐标点击或猜窗口句柄。
- 选中新写入行优先使用表格对象能力，例如 `sheet.select_rows([...])`；具体参数形态以当前影刀版本源码或运行结果为准，未验证时标注“需运行验证”。

## 7. 验证说明

- 本地读表或单测通过，只能说明后台数据处理逻辑可用。
- 涉及 WPS / Office 界面、公式刷新、宏、弹窗、文件占用时，最终仍需在影刀编辑器或真实运行环境验证。
- 不要把本地 pytest 或脚本运行通过写成“已在影刀编辑器内验证通过”。

## 8. 日期表缺失时优先按模板补齐

- 按日期批量扫描表格时，遇到某天文件缺失，不要默认静默跳过；先确认项目是否有模板资源，例如 `package.resources["base.xlsx"]`。
- 如果业务要求日期表连续，优先从模板复制生成缺失日期文件，再继续扫描和写入，避免后续统计因为缺表少算数据。
- 创建失败或模板缺失时，把日期、目标路径和错误原因放入 `scan_errors` 或同类结果列表，供最终汇总提示；不要只写一条模糊日志。
- 只有业务明确允许“缺表即无数据”时，才可以跳过，并在汇总里说明跳过日期。

## 9. ZIP 导出包含多个 xlsx 时先确认目标文件

- 平台导出 ZIP 后如果包含多个 `.xlsx`，不要随手取第一个文件；文件排序可能受压缩包内部顺序影响，不稳定。
- 可优先按业务文件名关键词、表头结构、sheet 名等规则识别目标报表；没有稳定结构时，再考虑选择体积最大的 `.xlsx` 作为临时策略并标注依据。
- 解压和选择结果应写入日志，至少包含 ZIP 文件名、候选 xlsx 列表和最终选中的文件，方便后续排查导入错表。
- 如果无法判断哪个表才是目标报表，应抛出明确异常或进入失败结果，不要继续用不确定文件写入业务表。
