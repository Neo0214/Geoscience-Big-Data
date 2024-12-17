# 预处理
from turtledemo.penrose import start

from openpyxl.styles import Color

from utils.Metadata import Column, TimeSegment
from utils.DataLoader import DataLoader
from tqdm import tqdm

data = DataLoader().load_data()
f=open("filter-data.txt","w")
for line in tqdm(data):
    # 若三元组有两个空值，则删除该三元组
    is_null_start = 1 if (line[Column.start_time.value] == "" or line[Column.start_time.value] == "00:00:00") else 0
    is_null_end = 1 if line[Column.end_time.value] == "" or line[Column.end_time.value] == "00:00:00" else 0
    is_null_dur = 1 if line[Column.raw_dur.value] == "" or int(line[Column.raw_dur.value]) <= 0 else 0
    if is_null_dur==1:
        print(f"Invalid raw_dur: {line[Column.raw_dur.value]}")
    if is_null_end + is_null_start + is_null_dur >= 2:
        data.remove(line)
        continue
    elif is_null_end + is_null_start + is_null_dur == 0:
        f.write(" ".join(line) + "\n")
        continue
    if is_null_end == 1:  # 通话结束时间为空
        # 用开始时间和通话时长计算结束时间
        start_time = line[Column.start_time.value].split(":")
        raw_dur = int(line[Column.raw_dur.value])
        end_time_seconds = int(start_time[0]) * 3600 + int(start_time[1]) * 60 + int(start_time[2]) + raw_dur
        end_time = str(end_time_seconds // 3600).zfill(2) + ":" + str(end_time_seconds % 3600 // 60).zfill(
            2) + ":" + str(end_time_seconds % 60).zfill(2)
        line[Column.end_time.value] = end_time
        f.write(" ".join(line) + "\n")
    elif is_null_start == 1:  # 开始时间为空
        # 用结束时间和通话时长计算开始时间
        end_time = line[Column.end_time.value].split(":")
        raw_dur = int(line[Column.raw_dur.value])
        start_time_seconds = int(end_time[0]) * 3600 + int(end_time[1]) * 60 + int(end_time[2]) - raw_dur
        start_time = str(start_time_seconds // 3600).zfill(2) + ":" + str(start_time_seconds % 3600 // 60).zfill(
            2) + ":" + str(start_time_seconds % 60).zfill(2)
        line[Column.start_time.value] = start_time
        f.write(" ".join(line) + "\n")
    elif is_null_dur == 1:  # 通话时长为空
        # 用开始时间和结束时间计算通话时长
        start_time = line[Column.start_time.value].split(":")
        end_time = line[Column.end_time.value].split(":")
        if start_time[0]>end_time[0]: # 跨天
            raw_dur = ((24-int(start_time[0]))*3600+(60-int(start_time[1]))*60+(60-int(start_time[2]))+
                       (int(end_time[0])*3600+int(end_time[1])*60+int(end_time[2])))
        else:
            raw_dur = (int(end_time[0]) - int(start_time[0])) * 3600 + (int(end_time[1]) - int(start_time[1])) * 60 + (
                        int(end_time[2]) - int(start_time[2]))
        line[Column.raw_dur.value] = str(raw_dur)
        f.write(" ".join(line) + "\n")



