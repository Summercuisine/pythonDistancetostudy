import os
import json
import re
import time

# 定义课程目录
path = "./"

# 获取课程目录下所有的文件名
file_names = [filename for filename in os.listdir(path) if re.match(r"^\d+-", filename)]

# 将文件名转换为序号和完整文件名的字典
name_dict = {}
for file_name in file_names:
    num_str, name = re.split(r"-", file_name, maxsplit=1)
    name_dict[int(num_str)] = file_name

# 定义打卡记录文件名和路径
record_dir = "学习打卡记录文件夹"
if not os.path.exists(record_dir):
    os.mkdir(record_dir)

if os.listdir(record_dir):
    # 如果有历史打卡记录，则获取最新的一条记录的时间
    last_record_file = sorted(os.listdir(record_dir))[-1]
    with open(os.path.join(record_dir, last_record_file), "r") as f:
        last_record_time = json.load(f)["time"]
else:
    # 如果没有历史打卡记录，则将默认时间设为当前时间
    last_record_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 输入当前学习的序号，并进行合法性检查
current_num = 0
while current_num not in name_dict:
    current_num = int(input(f"请输入当前学习的序号（{', '.join(map(str, sorted(name_dict.keys())))}）："))
current_file = name_dict[current_num]

# 记录学习时间并生成打卡记录文件名
current_time = time.time()
time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))
if last_record_time == time_str:
    record_filename = "学习python的第一天记录.json"
else:
    record_filename = f"学习python的第{(current_time - time.mktime(time.strptime(last_record_time, '%Y-%m-%d %H:%M:%S'))) // 86400 + 1}天记录.json"
record_path = os.path.join(record_dir, record_filename)

# 将本次打卡记录加入历史记录，并写入文件
record = {"file": current_file, "time": time_str}
with open(record_path, "w") as f:
    json.dump(record, f, ensure_ascii=False, indent=4)

print("打卡成功！")
