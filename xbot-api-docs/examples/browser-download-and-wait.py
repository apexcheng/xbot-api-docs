"""点击网页下载按钮，并等待本次文件下载完成。

运行前提：
- 本文件应放在影刀项目代码目录中运行
- 当前项目已安装市场指令：增强工具2026（xbot_enhance_tools）
- `args` 中的 url、download_button_xpath、filename_pattern 由影刀编辑器提前配置
- 下载按钮 XPath 需按当前页面实际情况确认
"""

import time

import xbot
from xbot.app import logging
from xbot_extensions.xbot_enhance_tools.browser_utils import wait_download_file


def main(args):
    """打开页面，点击下载按钮，并返回下载完成后的文件路径。

    :param args: 影刀流程初始化参数字典
    :type args: dict
    :return: 下载完成后的文件路径
    :rtype: str
    """
    url = args["url"]
    download_button_xpath = args["download_button_xpath"]
    filename_pattern = args.get("filename_pattern") or "*.xlsx"
    download_dir = args.get("download_dir") or None
    timeout = int(args.get("timeout") or 300)

    page = xbot.web.create(url=url, mode="chrome", load_timeout=60)
    page.wait_load_completed(timeout=30)

    start_time = time.time()
    page.find_by_xpath(download_button_xpath, timeout=20).click()

    try:
        file_path = wait_download_file(download_dir=download_dir, filename_pattern=filename_pattern, timeout=timeout, start_time=start_time)
    except TimeoutError as error:
        raise RuntimeError(f"等待下载超时：{filename_pattern}") from error

    logging.info(f"下载完成：{file_path}")
    return str(file_path)
