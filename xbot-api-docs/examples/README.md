# 最小可运行示例

`examples/` 目录存放最小、可直接复制运行的代码片段。

## 原则

- 优先简单、可复制、少封装
- 每个示例应能独立运行（假设影刀环境已就绪）
- 复杂逻辑拆成多个简单步骤，不要写成一个大函数

## 当前示例

- `project-entry-skeleton.py`：影刀项目入口骨架，说明固定导入、`main(args)` 和 `package.variables`
- `browser-bing-search.py`：最小浏览器搜索示例，演示打开页面、找元素、输入、点击
- `dingtalk-ai-table-records.py`：钉钉 AI 表格最小读写示例，演示读取 `data.records`、按 `record["fields"]` 取值和回写记录
- `dingtalk-markdown-notify.py`：钉钉群 Markdown 通知示例，演示 `dingtalk_bot_message.py_api.send_dingtalk_group()` 的最小调用
- `browser-price-check-single-row.py`：单行商品抓价并回写表格示例，演示 `xbot.web` 抓价、价格解析和钉钉 AI 表格更新
- `excel-clear-write-text.py`：清空指定数据区域后，把二维数组全部按文本批量写入，避免长数字精度丢失
- `excel-copy-range.py`：使用 `copy_range()` 和 `paste_range_ex()` 复制区域并保留格式、公式
- `browser-download-and-wait.py`：点击下载按钮后，使用 `wait_download_file()` 等待本次新文件完成

## 运行前提

- 这些示例假设代码运行在影刀项目内部，不是直接在本仓库里独立执行
- 影刀项目应已包含标准入口文件结构，可直接使用 `import xbot`、`from . import package`
- 如示例中使用 `xbot_extensions`，需确保对应市场指令已安装
- 如字段名、变量名、元素库名与当前项目不一致，应按项目实际情况调整

## 推荐阅读顺序

1. 先看 `project-entry-skeleton.py`，理解影刀编码版固定入口结构
2. 再看 `browser-bing-search.py`，理解最小网页操作链路
3. 再看 `dingtalk-ai-table-records.py`，理解钉钉 AI 表格读写返回结构
4. 需要群通知时看 `dingtalk-markdown-notify.py`
5. 需要业务串联时看 `browser-price-check-single-row.py`
6. 需要按文本更新 Excel 数据区域时看 `excel-clear-write-text.py`
7. 需要保留格式或公式复制区域时看 `excel-copy-range.py`
8. 需要点击网页按钮并等待下载时看 `browser-download-and-wait.py`

## 新增示例规范

1. 文件名：`{模块}-{场景}.py`，如 `browser-login.py`
2. 开头注释说明：影刀版本、依赖模块、运行前提
3. 代码尽量使用原生 API，不要引入过多自定义封装
4. 不确定的接口行为要标注“需运行验证”
