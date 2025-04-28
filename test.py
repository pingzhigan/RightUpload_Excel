import sys
import os
import time
import traceback
import winreg as reg

# 配置
MENU_NAME = '推送到PING的sql'
# 这个脚本本身的完整路径
SCRIPT_PATH = os.path.abspath(__file__)

# 检查注册表

def is_context_menu_registered():
    """检查右键菜单是否已注册"""
    try:
        with reg.OpenKey(reg.HKEY_CLASSES_ROOT, r'.xlsx') as key:
            file_type, _ = reg.QueryValueEx(key, '')

        shell_path = fr'{file_type}\shell\{MENU_NAME}'
        with reg.OpenKey(reg.HKEY_CLASSES_ROOT, shell_path):
            return True  # 能打开说明已经注册了
    except FileNotFoundError:
        return False

# 注册右键菜单
def register_context_menu():
    """注册右键菜单"""
    try:
        with reg.OpenKey(reg.HKEY_CLASSES_ROOT, '.xlsx') as key:
            file_type, _ = reg.QueryValueEx(key, '')

        shell_path = fr'{file_type}\shell\{MENU_NAME}'
        command_path = shell_path + r'\command'

        reg.CreateKey(reg.HKEY_CLASSES_ROOT, shell_path)
        reg.CreateKey(reg.HKEY_CLASSES_ROOT, command_path)

        python_exe = sys.executable  # 当前环境 Python 路径
        reg.SetValue(reg.HKEY_CLASSES_ROOT, shell_path, reg.REG_SZ, MENU_NAME)
        reg.SetValue(reg.HKEY_CLASSES_ROOT, command_path, reg.REG_SZ, f'"{python_exe}" "{SCRIPT_PATH}" "%1"')

        print(f"右键菜单 [{MENU_NAME}] 注册成功！")
    except Exception as e:
        print(f"注册右键菜单失败: {e}")
        input("按回车退出...")
        sys.exit(1)


def process_excel(file_path):
    """你的处理逻辑"""
    print(f"接收到文件路径：{file_path}")
    if not file_path.lower().endswith(('.xlsx', '.xls')):
        raise ValueError("选中的文件不是 Excel 表格！")
    print("正在处理 Excel 文件...")
    time.sleep(2)
    # 这里可以加你真正的处理逻辑，比如读取 Excel


def main():
    try:
        # 第一次运行时自动注册右键菜单
        if not is_context_menu_registered():
            print("检测到未注册右键菜单，正在注册...")
            register_context_menu()
            print("\n注册完成。请右键Excel文件重新使用。")
            input("按回车退出...")
            return

        # 正常执行
        if len(sys.argv) < 2:
            print("请通过右键菜单传入 Excel 文件。")
            input("按回车退出...")
            return

        excel_path = sys.argv[1]
        process_excel(excel_path)

    except Exception as e:
        print("发生错误：")
        traceback.print_exc()

    finally:
        input("\n处理结束，按回车键退出...")


if __name__ == "__main__":
    main()
