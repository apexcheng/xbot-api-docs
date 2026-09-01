"""影刀项目入口。"""

from xbot.app.dialog import show_custom_dialog
from xbot_extensions.xbot_enhance_tools.market_config import (
    dialog_result_to_dict,
    load_secret_config,
    save_secret_config,
)

from .config import CONFIG_PATH


def init_config():
    config = load_secret_config(str(CONFIG_PATH))
    if config:
        return config

    dialog_settings = {
        "dialogTitle": "初始化配置",
        "settings": {
            "editors": [
                {
                    "type": "TextBox",
                    "label": "账号",
                    "VariableName": "username",
                    "value": None,
                    "nullText": "请输入账号",
                },
                {
                    "type": "TextBox",
                    "label": "密码",
                    "VariableName": "password",
                    "value": None,
                    "nullText": "请输入密码",
                },
            ],
            "buttons": [
                {
                    "type": "Button",
                    "label": "保存并启动",
                    "theme": "red",
                    "hotkey": "Enter",
                },
                {
                    "type": "Button",
                    "label": "启动",
                    "theme": "white",
                },
                {
                    "type": "Button",
                    "label": "取消",
                    "theme": "white",
                    "hotkey": "Esc",
                },
            ],
        },
    }

    dialog_result = show_custom_dialog(dialog_settings)
    config = dialog_result_to_dict(dialog_result)

    action = config.get("pressed_button")
    if action == "取消":
        return None

    if action == "保存并启动":
        save_secret_config(str(CONFIG_PATH), config)

    return config


def main(args):
    config = init_config()

    if not config:
        return

    # TODO: 后续业务流程从 config 和已确认的 args 参数中取值。
