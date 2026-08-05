"""复制 Excel 已使用区域，并保留格式和公式。

运行前提：
- 本文件应放在影刀项目代码目录中运行
- `args` 中的 file_path、source_sheet_name、target_sheet_name 由影刀编辑器提前配置
- 当前电脑已安装 WPS；使用 Office 时把 kind 改为 "office"
"""

import xbot.excel
from xbot.app import logging


def main(args):
    """把源 Sheet 的已使用区域复制到目标 Sheet 的 A1。

    :param args: 影刀流程初始化参数字典
    :type args: dict
    """
    file_path = args["file_path"]
    source_sheet_name = args.get("source_sheet_name") or "源数据"
    target_sheet_name = args.get("target_sheet_name") or "目标数据"

    workbook = None
    try:
        workbook = xbot.excel.open(file_name=file_path, kind="wps", visible=True)
        source_sheet = workbook.get_sheet_by_name(source_sheet_name)
        target_sheet = workbook.get_sheet_by_name(target_sheet_name)

        end_row = source_sheet.get_first_free_row() - 1
        end_column = source_sheet.get_last_column()
        if end_row < 1:
            raise ValueError(f"源 Sheet「{source_sheet_name}」没有可复制的数据")

        source_sheet.copy_range(begin_row_num=1, begin_column_name="A", end_row_num=end_row, end_column_name=end_column)
        target_sheet.paste_range_ex(row_num=1, column_name="A")

        workbook.save()
        logging.info(f"已复制 {source_sheet_name}!A1:{end_column}{end_row} 到 {target_sheet_name}!A1")
    finally:
        if workbook:
            try:
                workbook.close()
            except Exception as error:
                logging.warning(f"关闭工作簿失败：{error}")
