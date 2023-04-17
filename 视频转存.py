import os
import re

# 视频所在目录
source_dir = r'D:\python学习视频\黑马程序员python教程，8天python从入门到精通，学python看这套就够了\黑马程序员python教程，8天python从入门到精通，学python看这套就够了'

# 目标目录
target_dir = r'G:\重启python学习路程'

# 匹配 1080P 高清-AVC 字眼的正则表达式
pattern = re.compile(r'(\d{4})[pP]\s*[高清HD]{2}\s*[-—–‐-]*\s*[AVC]*')

# 遍历视频目录下的所有文件
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.endswith('.mp4'):
            # 获取文件名和绝对路径
            filename = os.path.splitext(file)[0]
            abs_path = os.path.join(root, file)

            # 去掉视频名称中的 1080P 高清-AVC 字眼
            new_filename = re.sub(pattern, '', filename)

            # 创建新文件路径
            target_file = os.path.join(target_dir, new_filename + '.py')

            # 写入新的 Python 文件
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(f'# -*- coding: utf-8 -*-\n')
                f.write(f'# {new_filename}\n\n')
                f.write(f'print("Hello World!")\n')

            print(f'{abs_path} ==> {target_file}')
