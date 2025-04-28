import json
import os
import socket
import time

HOST = '172.16.2.50'
PORT = 5001
TIMEOUT = 40  # 客户端超时秒数（稍微长点）

file_path = '项目列表.xlsx'


def send_file(file_path):
    filesize = os.path.getsize(file_path)
    filename = os.path.basename(file_path)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(TIMEOUT)
        s.connect((HOST, PORT))

        # 发送文件名
        s.sendall(filename.encode())
        s.recv(1)

        # 发送文件大小
        s.sendall(str(filesize).encode())
        s.recv(1)

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

        # ---------------------------------
        # 上传完成后，接收服务器的处理结果
        # ---------------------------------
        response = s.recv(4096)
        response_json = json.loads(response.decode())

        print("\n服务器返回结果:")
        print(json.dumps(response_json, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    send_file(file_path)
