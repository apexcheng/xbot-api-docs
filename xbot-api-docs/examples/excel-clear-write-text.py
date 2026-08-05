"""清空 Excel 数据区域并全部按文本批量写入。

运行前提：
- 本文件应放在影刀项目代码目录中运行
- `args` 中的 file_path、sheet_name、rows 由影刀编辑器提前配置
- 当前电脑已安装 WPS；使用 Office 时把 kind 改为 "office"
"""

import xbot.excel
from xbot.app import logging


def main(args):
    """清空目标 Sheet 的旧数据，并把二维数组全部按文本写入。

    :param args: 影刀流程初始化参数字典
    :type args: dict
    """
    file_path = args["file_path"]
    sheet_name = args.get("sheet_name") or "数据"
    start_row = int(args.get("start_row") or 2)
    start_column = args.get("start_column") or "A"
    rows = args.get("rows") or [
        ["100149257095", "202608060001", 2],
    ]

    text_rows = []
    for row in rows:
        text_row = []
        for value in row:
            text = "" if value is None else str(value)
            text_row.append("'" + text if text else "")
        text_rows.append(text_row)

    workbook = None
    try:
        workbook = xbot.excel.open(file_name=file_path, kind="wps", visible=True)
        sheet = workbook.get_sheet_by_name(sheet_name)

        first_free_row = sheet.get_first_free_row()
        last_column = sheet.get_last_column()
        if first_free_row > start_row:
            sheet.clear_range(begin_row_num=start_row, begin_column_name=start_column, end_row_num=first_free_row, end_column_name=last_column, target="content")

        if text_rows:
            sheet.set_range(row_num=start_row, col_name=start_column, values=text_rows)

        workbook.save()
        logging.info(f"已写入 {len(text_rows)} 行数据，所有非空值均按文本保存")
    finally:
        if workbook:
            workbook.close()
