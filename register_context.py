import sys
import os
import winreg as reg


def is_context_menu_registered(menu_name='右键菜单名称'):
    """检查右键菜单是否已注册"""
    try:
        with reg.OpenKey(reg.HKEY_CLASSES_ROOT, r'.xlsx') as key:
            file_type, _ = reg.QueryValueEx(key, '')
        shell_path = fr'{file_type}\shell\{menu_name}'
        with reg.OpenKey(reg.HKEY_CLASSES_ROOT, shell_path):
            return True
    except FileNotFoundError:
        return False


def register_context_menu(menu_name='右键菜单名称'):
    """注册右键菜单（自动适配开发与打包环境）"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        exe_path = os.path.join(base_dir, 'upload_excel.exe')
        py_path = os.path.join(base_dir, 'upload_excel.py')

        if os.path.exists(exe_path):
            # 打包环境：优先使用 .exe
            command = f'"{exe_path}" "%1"'
            print(f"[打包模式] 使用可执行文件注册：{exe_path}")
        elif os.path.exists(py_path):
            # 开发环境：使用 python 解释器运行 .py
            python_exe = sys.executable
            command = f'"{python_exe}" "{py_path}" "%1"'
            print(f"[开发模式] 使用 Python 脚本注册：{py_path}")
        else:
            print("[错误] 未找到 upload_excel.exe 或 upload_excel.py，无法注册菜单")
            return

        # 获取 .xlsx 文件类型（如 Excel.Sheet.12）
        with reg.OpenKey(reg.HKEY_CLASSES_ROOT, '.xlsx') as key:
            file_type, _ = reg.QueryValueEx(key, '')

        shell_path = fr'{file_type}\shell\{menu_name}'
        command_path = shell_path + r'\command'

        # 写入注册表
        reg.CreateKey(reg.HKEY_CLASSES_ROOT, shell_path)
        reg.CreateKey(reg.HKEY_CLASSES_ROOT, command_path)

        reg.SetValue(reg.HKEY_CLASSES_ROOT, shell_path, reg.REG_SZ, menu_name)
        reg.SetValue(reg.HKEY_CLASSES_ROOT, command_path, reg.REG_SZ, command)

        print(f"[注册成功] 已注册右键菜单：{menu_name}")
    except PermissionError:
        print("[错误] 注册失败：请使用管理员权限运行")
    except Exception as e:
        print(f"[错误] 注册失败：{e}")


def unregister_context_menu(menu_name='右键菜单名称'):
    """注销右键菜单"""
    try:
        with reg.OpenKey(reg.HKEY_CLASSES_ROOT, '.xlsx') as key:
            file_type, _ = reg.QueryValueEx(key, '')
        shell_path = fr'{file_type}\shell\{menu_name}'

        reg.DeleteKey(reg.HKEY_CLASSES_ROOT, shell_path + r'\command')
        reg.DeleteKey(reg.HKEY_CLASSES_ROOT, shell_path)

        print(f"[注销成功] 已移除右键菜单：{menu_name}")
    except FileNotFoundError:
        print("[提示] 菜单不存在，可能已删除")
    except PermissionError:
        print("[错误] 注销失败：需要以管理员身份运行")
    except Exception as e:
        print(f"[错误] 注销右键菜单失败：{e}")


def main():
    print("=== Excel (.xlsx) 右键菜单注册工具 ===")
    menu_name = input("请输入右键菜单名称（如：上传Excel）：").strip()
    if not menu_name:
        print("菜单名称不能为空！")
        return

    if is_context_menu_registered(menu_name):
        print(f"[检查] 当前菜单 [{menu_name}] 已注册。")
    else:
        print(f"[检查] 当前菜单 [{menu_name}] 未注册。")

    action = input("请选择操作：[r] 注册 / [u] 注销 / [q] 退出：").strip().lower()

    if action == 'r':
        register_context_menu(menu_name)
    elif action == 'u':
        unregister_context_menu(menu_name)
    elif action == 'q':
        print("已退出。")
    else:
        print("无效的操作指令。")


if __name__ == '__main__':
    main()
