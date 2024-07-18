# -*- coding: utf-8 -*-
import os
import shutil
import time
from img import media_path
# 图片存储路径
# media_path = "/www/wwwroot/huione_py/public/image/"
"""
    计划任务shell脚本配置每天执行一次
    脚本内容为：
    #!/bin/bash
    python37  /www/wwwroot/huione_py/image_file.py
"""


def delete_dirs(dir_path):
    # 获取目录下的所有文件和目录
    all_files = os.listdir(dir_path)

    neglect_dir = get_file_dir_name()
    print("delete_dirs directory: neglect_dir ", neglect_dir)
    # 遍历目录路径列表，并删除每个目录
    for file_name in all_files:
        # 构造目录或文件的完整路径
        full_path = os.path.join(dir_path, file_name)

        # 如果是目录则递归处理
        if os.path.isdir(full_path) and neglect_dir != file_name:
            print("delete_dirs directory: ", full_path)
            shutil.rmtree(full_path)  # 删除目录


def get_file_dir_name():
    return str(time.strftime("%Y_%m_%d", time.localtime()))


def main():
    # 获取所有目录并删除
    dir_path = media_path

    delete_dirs(dir_path)


if __name__ == '__main__':
    print("init...")
    main()
