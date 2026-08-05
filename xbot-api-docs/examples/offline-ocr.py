"""使用离线 OCR 识别图片文字。

运行前提：
- 当前项目已安装 activity_179ea575
- `args` 提供 image_path
"""

from xbot_extensions import activity_179ea575


def main(args):
    """识别图片并返回完整 OCR 结果。

    :param args: 影刀流程初始化参数字典
    :type args: dict
    :return: OCR 结果
    """
    result = activity_179ea575.process1(图片路径或图片url=args["image_path"], 输出完整结果=True, 文字检测框过滤的阈值=0.4, 文字检测框的大小=1)
    if not result:
        raise RuntimeError("OCR 未识别到文字")
    return result
