# 小工具指令集 (activity_47680f64)

> 调用类型：`both`  
> 主要入口：Code 型直接调用业务 .py 的 main()；Visual 型通过 __init__.py 的 processN() 调用 xbot_visual.process.run()。  
> 证据边界：入口和参数以当前安装版本的 `package.json`、公开包装函数及运行结果为准。
> 返回：[市场指令索引](../extension-instructions.md)

---

**目录/指令名：** `activity_47680f64` / 小工具指令集

**调用方式：** both（flow + direct python）

**用途：** 文件操作、日期处理、邮件获取、验证码获取

**调用入口：**
- Flow：`xbot_extensions.activity_47680f64.process1()` ~ `process5()`
- Direct：`CreateDir.main()`、`MoveToPardir.main()`、`DateStringCheck.main()`、`latest_email.main()`、`get_SMS_code.main()`

**参数说明：**
- `process2(是否弹窗下载, 保存文件夹, 文件名, 下载前文件数量, 浏览器下载保存路径, 最大等待时长)`

**默认值：**
- 浏览器下载保存路径：默认 `$HOME/Downloads`

**注意事项：**
- Code 型指令直接调用 `.py` 中的 `main()`，不是 `__init__.py` 中的包装函数
- Visual 型指令（process1~5）通过 `__init__.py` 包装调用
- `latest_email.py` 支持 163 邮箱，需要 email + password
- `get_SMS_code.py` 需要配置验证码获取接口 URL

**典型调用方式：**
```python
# Flow 型
xbot_extensions.activity_47680f64.process2(
    是否弹窗下载=False,
    保存文件夹="/save",
    文件名="file.zip",
    下载前文件数量=0,
    浏览器下载保存路径="",
    最大等待时长=30
)
```

---
