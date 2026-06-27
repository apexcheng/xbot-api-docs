import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent


def resolve_project_dir(project_dir=None):
    """Resolve the target ShadowBot project directory.

    :param str|None project_dir: Optional project directory.
    :return pathlib.Path: Resolved project directory.
    """
    if project_dir:
        path = Path(project_dir).expanduser().resolve()
    else:
        path = Path.cwd().resolve()

    if not path.exists():
        raise FileNotFoundError(f"目标项目目录不存在：{path}")

    package_json_path = path / "package.json"
    if not package_json_path.exists():
        raise FileNotFoundError(f"目标项目目录缺少 package.json：{package_json_path}")

    return path


def load_package_json(project_dir):
    """Load `package.json` as a Python object.

    :param pathlib.Path project_dir: Target project directory.
    :return dict: Parsed package metadata.
    """
    package_json_path = project_dir / "package.json"
    with package_json_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_package_json(project_dir, package_data):
    """Write package metadata back to `package.json`.

    :param pathlib.Path project_dir: Target project directory.
    :param dict package_data: Updated package metadata.
    """
    package_json_path = project_dir / "package.json"
    with package_json_path.open("w", encoding="utf-8") as f:
        json.dump(package_data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def normalize_python_file_name(file_name):
    """Normalize a Python file path into file and flow names.

    :param str file_name: Python file name.
    :return tuple[str, str]: `(file_name, flow_name)`.
    """
    path = Path(file_name)
    if path.suffix != ".py":
        raise ValueError(f"只支持 .py 文件：{file_name}")
    return path.name, path.stem


def resolve_existing_group_name(package_data, group_name):
    """Use an existing flow-group name if it already exists.

    :param dict package_data: Package metadata.
    :param str group_name: Requested group name.
    :return str: Existing or requested group name.
    """
    for item in package_data.get("flow_groups", []):
        if item.get("name") == group_name:
            return item["name"]
    return group_name


def ensure_group_exists(package_data, group_name):
    """Make sure the requested group exists in `flow_groups`.

    :param dict package_data: Package metadata.
    :param str group_name: Group name to add.
    :return str: Final group name.
    """
    group_name = resolve_existing_group_name(package_data, group_name)

    for item in package_data.get("flow_groups", []):
        if item.get("name") == group_name:
            return group_name

    package_data.setdefault("flow_groups", []).append({"name": group_name})
    return group_name


def ensure_code_flow(package_data, file_name, group_name=None):
    """Ensure a Python file is registered as a ShadowBot Code flow.

    :param dict package_data: Package metadata.
    :param str file_name: Python file name.
    :param str group_name: Target flow group.
    :return dict: Summary of the registration result.
    """
    py_name, flow_name = normalize_python_file_name(file_name)
    existing_flow = None
    for flow in package_data.get("flows", []):
        if flow.get("filename") == flow_name:
            existing_flow = flow
            break

    target_group_name = None
    if group_name is not None:
        target_group_name = ensure_group_exists(package_data, group_name)

    if existing_flow:
        existing_flow["name"] = flow_name
        existing_flow["filename"] = flow_name
        existing_flow["kind"] = "Code"
        existing_flow["opened"] = False
        if group_name is not None:
            existing_flow["groupName"] = target_group_name
        existing_flow["enableCopilot"] = False
        return {
            "file": py_name,
            "flow": flow_name,
            "group": existing_flow.get("groupName"),
            "action": "updated",
        }

    new_flow = {
        "name": flow_name,
        "filename": flow_name,
        "kind": "Code",
        "opened": False,
        "groupName": target_group_name,
        "enableCopilot": False,
    }
    package_data.setdefault("flows", []).append(new_flow)
    return {
        "file": py_name,
        "flow": flow_name,
        "group": new_flow.get("groupName"),
        "action": "created",
    }


def create_backup(project_dir, files):
    """Create a timestamped backup folder under `backups/`.

    :param pathlib.Path project_dir: Target project directory.
    :param list[str] files: Files to copy into the backup.
    :return tuple[pathlib.Path, list[str]]: Backup directory and copied file names.
    """
    backup_dir = project_dir / "backups" / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    for file_name in files:
        source = project_dir / file_name
        if not source.exists():
            raise FileNotFoundError(f"找不到文件：{source}")
        shutil.copy2(source, backup_dir / source.name)
        copied.append(source.name)

    return backup_dir, copied


def find_shadowbot_python():
    """Locate the ShadowBot Python interpreter.

    :return pathlib.Path: Python executable path.
    """
    candidates = [
        ROOT_DIR.parent / "venv310" / "Scripts" / "python.exe",
        Path(sys.executable),
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError("未找到可用的 Python 解释器")


def compile_files(project_dir, files):
    """Compile files with the ShadowBot interpreter.

    :param pathlib.Path project_dir: Target project directory.
    :param list[str] files: Files to compile.
    :return pathlib.Path: Python executable used for compilation.
    """
    python_exe = find_shadowbot_python()
    command = [str(python_exe), "-m", "py_compile", *files]
    subprocess.run(command, cwd=project_dir, check=True)
    return python_exe


def show_flow(package_data, file_name):
    """Get the flow entry for a Python file.

    :param dict package_data: Package metadata.
    :param str file_name: Python file name.
    :return dict|None: Matching flow entry if found.
    """
    _, flow_name = normalize_python_file_name(file_name)
    for flow in package_data.get("flows", []):
        if flow.get("filename") == flow_name:
            return flow
    return None


def command_backup(args):
    """Run the `backup` command."""
    project_dir = resolve_project_dir(args.project_dir)
    backup_dir, copied = create_backup(project_dir, args.files)
    print(f"backup_dir={backup_dir}")
    for item in copied:
        print(f"copied={item}")


def command_ensure_flow(args):
    """Run the `ensure-flow` command."""
    project_dir = resolve_project_dir(args.project_dir)
    package_data = load_package_json(project_dir)
    results = []
    for file_name in args.files:
        results.append(ensure_code_flow(package_data, file_name, args.group))
    save_package_json(project_dir, package_data)

    for result in results:
        print(
            f"{result['action']} flow:"
            f" file={result['file']}, flow={result['flow']}, group={result['group']}"
        )


def command_compile(args):
    """Run the `compile` command."""
    project_dir = resolve_project_dir(args.project_dir)
    python_exe = compile_files(project_dir, args.files)
    print(f"compiled_with={python_exe}")


def _find_imported_modules(src_text):
    """Return module stem names found in source text import statements."""
    imported = set()
    for line in src_text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("from ", "import ")):
            try:
                parts = stripped.split()
                if stripped.startswith("from "):
                    # from . import package or from .module import name
                    if len(parts) >= 2:
                        name = parts[1].lstrip(".").split(".")[0]
                        if name and name not in (
                            "xbot", "xbot_extensions", "package",
                            "sys", "os", "re", "json", "datetime", "typing",
                        ):
                            imported.add(name)
                else:  # import module
                    name = parts[1].split(".")[0].split("(")[0].strip()
                    if name and name not in (
                        "xbot", "xbot_extensions", "package",
                        "sys", "os", "re", "json", "datetime", "typing",
                    ):
                        imported.add(name)
            except Exception:
                pass
    return imported


def _discover_helper_modules(project_dir, entry_files):
    """Find non-entry *.py files that are imported by entry files.

    An entry file like run.py imports helpers with relative imports
    (e.g. from .constants import ...).  We find all .py files in project_dir,
    check which ones are imported by any entry file, and return those that
    are not entry_files themselves.
    """
    entry_stems = {Path(f).stem for f in entry_files}
    # Scan every .py in the project_dir to build a name->filename map
    name_to_file = {}
    for py_file in project_dir.glob("*.py"):
        stem = py_file.stem
        if stem not in name_to_file:
            name_to_file[stem] = py_file.name

    helpers = []
    for fname in entry_files:
        src_path = project_dir / fname
        if not src_path.exists():
            continue
        src = src_path.read_text(encoding="utf-8")
        imported = _find_imported_modules(src)
        for name in imported:
            if name in name_to_file and name not in entry_stems:
                helpers.append(name_to_file[name])

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for h in helpers:
        if h not in seen:
            seen.add(h)
            unique.append(h)
    return unique


def _discover_unregistered_python_files(project_dir, package_data):
    """Find project Python files that are not registered as Code flows.

    :param pathlib.Path project_dir: Target project directory.
    :param dict package_data: Package metadata.
    :return list[str]: Unregistered Python file names.
    """
    registered = {
        f"{flow.get('filename')}.py"
        for flow in package_data.get("flows", [])
        if flow.get("filename")
    }
    files = []
    for py_file in sorted(project_dir.glob("*.py")):
        if py_file.name == "package.py":
            continue
        if py_file.name not in registered:
            files.append(py_file.name)
    return files


def command_prepare(args):
    """Run the common external-edit workflow.

    It ensures the flows exist and compiles them.
    Helper modules imported by entry .py files are automatically discovered and compiled too.
    """
    project_dir = resolve_project_dir(args.project_dir)

    # Discover helper modules imported by the entry files
    helpers = _discover_helper_modules(project_dir, args.files)

    package_data = load_package_json(project_dir)
    all_flow_files = list(dict.fromkeys(
        args.files + _discover_unregistered_python_files(project_dir, package_data)
    ))
    results = []
    for file_name in all_flow_files:
        results.append(ensure_code_flow(package_data, file_name, args.group))
    save_package_json(project_dir, package_data)

    # Compile entry files + discovered helpers
    to_compile = list(dict.fromkeys(args.files + helpers))
    python_exe = compile_files(project_dir, to_compile)

    for result in results:
        print(
            f"{result['action']} flow:"
            f" file={result['file']}, flow={result['flow']}, group={result['group']}"
        )
    if helpers:
        print(f"helpers_compiled={helpers}")
    print(f"compiled_with={python_exe}")


def command_show_flow(args):
    """Run the `show-flow` command."""
    project_dir = resolve_project_dir(args.project_dir)
    package_data = load_package_json(project_dir)
    flow = show_flow(package_data, args.file)
    if not flow:
        print(f"not_found={args.file}")
        return

    print(json.dumps(flow, ensure_ascii=False, indent=2))


def build_parser():
    """Build the CLI parser.

    :return argparse.ArgumentParser: Configured parser instance.
    """
    parser = argparse.ArgumentParser(
        description="将外部修改的影刀项目代码同步到影刀编辑器的工具。"
    )
    parser.add_argument(
        "--project-dir",
        default=None,
        help="目标影刀项目目录；不传时默认使用当前工作目录",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_backup = subparsers.add_parser("backup", help="备份指定文件")
    parser_backup.add_argument("files", nargs="+", help="要备份的文件名")
    parser_backup.set_defaults(func=command_backup)

    parser_ensure_flow = subparsers.add_parser("ensure-flow", help="确保代码文件已登记到 package.json")
    parser_ensure_flow.add_argument("files", nargs="+", help="要登记的 .py 文件")
    parser_ensure_flow.add_argument("--group", default=None, help="flow 分组名；不传则保留已有分组")
    parser_ensure_flow.set_defaults(func=command_ensure_flow)

    parser_compile = subparsers.add_parser("compile", help="用影刀 Python 编译指定文件")
    parser_compile.add_argument("files", nargs="+", help="要编译的文件名")
    parser_compile.set_defaults(func=command_compile)

    parser_prepare = subparsers.add_parser(
        "prepare",
        help="外部改完代码后的常用收尾：登记 flow、编译",
    )
    parser_prepare.add_argument("files", nargs="+", help="刚刚修改过的 .py 文件")
    parser_prepare.add_argument("--group", default=None, help="flow 分组名；不传则保留已有分组")
    parser_prepare.set_defaults(func=command_prepare)

    parser_show_flow = subparsers.add_parser("show-flow", help="查看某个 .py 文件对应的 flow 配置")
    parser_show_flow.add_argument("file", help="要查看的 .py 文件")
    parser_show_flow.set_defaults(func=command_show_flow)

    return parser


def main():
    """Program entry point."""
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
