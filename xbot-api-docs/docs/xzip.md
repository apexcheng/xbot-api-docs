# 影刀压缩解压方法

> 定位：影刀 / xbot 的 ZIP 压缩与解压接口。
> 说明：本页整理 `xbot.xzip` 模块的公开方法，依赖 7za 工具。

---

## 1. 核验来源

本页按 ShadowBot 6.3.12 内置 `xbot/xzip.py` 核对。安装目录随版本变化；其他版本用 `inspect.getfile(xbot.xzip)` 定位当前实现。

---

## 2. 依赖说明

- Windows 下默认使用当前工作目录里的 `7za.exe`。
- 非 Windows 下从环境变量 `SHADOWBOT_7ZA_PATH` 获取 7za 路径。
- 若找不到 7za，会直接报错。

---

## 3. `zip(file_folder_path, zip_file_path, *, compress_level=5, password=None)`

### 作用

压缩文件或文件夹为 zip。

### 参数

| 参数名 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `file_folder_path` | `str` / `list[str]` | 是 | 待压缩文件或文件夹 |
| `zip_file_path` | `str` | 是 | 输出 zip 路径 |
| `compress_level` | `int` | 否 | 压缩级别 1~9，默认 5 |
| `password` | `str` / `None` | 否 | 压缩密码 |

### 返回值

无。

### 常用场景

- 打包多个文件
- 导出压缩包
- 带密码打包

### 注意事项

- `file_folder_path` 不能为空。
- 输出文件已存在时会报错。
- 压缩失败会抛出 `EngineError`。

### 示例

```python
from xbot import xzip

xzip.zip([r"C:\a.txt", r"C:\b.txt"], r"C:\out.zip", compress_level=5)
```

---

## 4. `unzip(zip_file_path, unzip_dir_path, *, password=None)`

### 作用

解压 zip 文件到指定目录。

### 参数

| 参数名 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `zip_file_path` | `str` | 是 | zip 文件路径 |
| `unzip_dir_path` | `str` | 是 | 解压目录 |
| `password` | `str` / `None` | 否 | 解压密码 |

### 返回值

无。

### 注意事项

- zip 文件不存在时会报错。
- 解压失败会抛出 `EngineError`。
- 解压路径是否自动创建，源码未显式确认，建议运行验证。

### 示例

```python
from xbot import xzip

xzip.unzip(r"C:\out.zip", r"C:\out")
```

---

## 5. 使用建议

- 压缩前先确认目标文件不存在，避免覆盖失败。
- 跨平台脚本要先确认 7za 路径是否可用。
- 需要密码时，压缩和解压都要保持密码一致。
