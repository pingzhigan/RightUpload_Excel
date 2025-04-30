import configparser
import json
import os
import socket
import sys
import time
import traceback


class FileUploader:
    def __init__(self, config_path='config.ini'):
        self.config_path = config_path
        self.host = None
        self.port = None
        self.timeout = None
        self._load_config()

    def _load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        try:
            self.host = config.get('server', 'host')
            self.port = config.getint('server', 'port')
            self.timeout = config.getint('server', 'timeout')
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
            raise RuntimeError(f"配置文件读取失败: {e}")

    def send_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        filesize = os.path.getsize(file_path)
        filename = os.path.basename(file_path)

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                print(f"连接到服务器 {self.host}:{self.port} ...")
                s.connect((self.host, self.port))

                # 发送文件名
                s.sendall(filename.encode())
                if not s.recv(1):
                    raise ConnectionError("服务器未响应文件名确认")

                # 发送文件大小
                s.sendall(str(filesize).encode())
                if not s.recv(1):
                    raise ConnectionError("服务器未响应文件大小确认")

                print(f"开始上传 {filename} ({filesize} bytes)")
                start_time = time.time()

                sent = 0
                with open(file_path, 'rb') as f:
                    while sent < filesize:
                        data = f.read(4096)
                        if not data:
                            break
                        s.sendall(data)
                        sent += len(data)
                        progress = sent / filesize * 100
                        print(f"\r上传进度: {progress:.2f}% ({sent}/{filesize} bytes)", end='')

                duration = time.time() - start_time
                print(f"\n上传完成，用时 {duration:.2f}s")

                # 接收服务器处理结果
                response = s.recv(4096)
                if not response:
                    raise ValueError("未收到服务器返回数据")

                response_json = json.loads(response.decode())
                print("\n服务器返回结果:")
                print(json.dumps(response_json, indent=2, ensure_ascii=False))
                return response_json

        except socket.timeout:
            print("连接超时，请检查网络或服务器状态")
        except ConnectionError as e:
            print(f"连接错误: {e}")
        except json.JSONDecodeError:
            print("服务器返回的不是有效的 JSON")
        except Exception as e:
            print(f"发生错误: {e}")


def main():
    try:
        # 正常执行
        if len(sys.argv) < 2:
            print("请通过右键菜单传入 Excel 文件。")
            input("按回车退出...")
            return

        excel_path = sys.argv[1]
        # 调用上传方法
        fileuploader = FileUploader()
        res = fileuploader.send_file(excel_path)
        # 可执行下一步操作

    except Exception as e:
        print(f"发生错误：{e}")
        traceback.print_exc()
    finally:
        input("\n处理结束，按回车键退出...")

if __name__ == '__main__':
    main()