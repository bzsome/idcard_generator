import os
import sys


def get_assets_path(relative_path):
    """获取资源的绝对路径，无论是在开发环境还是在打包后的环境中。"""
    base_path = get_base_path()
    return os.path.join(base_path, "assets", relative_path)


def get_resource_path(relative_path):
    """获取资源的绝对路径，无论是在开发环境还是在打包后的环境中。"""
    base_path = get_base_path()
    return os.path.join(base_path, relative_path)


def get_base_path():
    if hasattr(os, '__builtins__'):
        if '__nuitka_binary_dir' in os.__builtins__:
            return os.__builtins__['__nuitka_binary_dir']

    # 打包后，资源文件会被放在 sys._MEIPASS 目录下
    if hasattr(sys, '_MEIPASS'):
        # 单个exe解药后的路径
        base_path = sys._MEIPASS
    else:
        # 开发环境下，资源文件相对于脚本文件
        base_path = os.path.abspath(".")
    return base_path


def print_sys_info():
    print("has_frozen", hasattr(sys, "frozen"))
    print("__nuitka__", '__nuitka__' in globals())

    print("print_sys_info:sys")
    for name, value in vars(sys).items():
        print(f"{name}: {value}")

    print("\n\n\n\n====================>>>>>>>>>>>>>>>>>>>>>>>")
    print("print_sys_info:os")
    for name, value in vars(os).items():
        print(f"{name}: {value}")
