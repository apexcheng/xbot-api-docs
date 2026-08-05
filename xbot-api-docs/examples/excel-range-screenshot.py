"""把 Excel / WPS 指定区域保存为图片。

运行前提：
- 当前项目已安装 Excel扩展操作（activity_excel_v2）
- `args` 提供 target_file_path、sheet_name、image_path
"""

import xbot.excel
from xbot_extensions.activity_excel_v2 import process24 as excel_range_screenshot


def main(args):
    """截取当前 Sheet 的已使用区域。

    :param args: 影刀流程初始化参数字典
    :type args: dict
    :return: 图片保存路径
    :rtype: str
    """
    workbook = xbot.excel.open(file_name=args["target_file_path"], kind="wps", visible=True)
    try:
        sheet = workbook.get_sheet_by_name(args["sheet_name"])
        last_row = sheet.get_first_free_row() - 1
        last_column = sheet.get_last_column()
        if last_row < 1:
            raise ValueError(f"Sheet「{sheet.get_name()}」没有可截图的数据")
        result = excel_range_screenshot(excel_instance=workbook, begin_row=1, begin_column="A", end_row=last_row, end_column=last_column, save_path=args["image_path"], sheet_name=sheet.get_name())
        if isinstance(result, dict):
            return result.get("image_save_path", args["image_path"])
        return result or args["image_path"]
    finally:
        workbook.close()
