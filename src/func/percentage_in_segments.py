from turtledemo.penrose import start

from utils.Metadata import Column, TimeSegment
from utils.DataLoader import DataLoader
from utils.DataWriter import DataWriter
from tqdm import tqdm


def calc(result_line):
    total_time=sum(result_line[1:])
    for i in range(1, 9):
        result_line[i] = result_line[i] / float(total_time)


def add_value(result_line, start_seconds, end_seconds):
    start_time_zone = start_seconds // 10800  # 开始时间所在时间段 index
    end_time_zone = end_seconds // 10800  # 结束时间所在时间段 index
    if start_time_zone == end_time_zone:
        result_line[start_time_zone + 1] += (end_seconds - start_seconds)
    else:  # 通话时间跨时段
        result_line[start_time_zone + 1] += (start_time_zone + 1) * 10800 - start_seconds
        result_line[end_time_zone + 1] += (end_seconds - end_time_zone * 10800)
        for i in range(start_time_zone + 1, end_time_zone):
            result_line[i + 1] += 10800


def update_time_value(result_line, start_time, end_time):
    start_time = start_time.split(":")
    end_time = end_time.split(":")
    if int(end_time[0]) >= 24:
        end_time[0] = str(int(end_time[0]) - 24)
    if int(end_time[0]) >= int(start_time[0]):  # 通话时间没有跨天
        start_seconds = int(start_time[0]) * 3600 + int(start_time[1]) * 60 + int(start_time[2])
        end_seconds = int(end_time[0]) * 3600 + int(end_time[1]) * 60 + int(end_time[2])
        add_value(result_line, start_seconds, end_seconds)
    else:  # 跨天
        start_seconds = int(start_time[0]) * 3600 + int(start_time[1]) * 60 + int(start_time[2])
        end_seconds = int(end_time[0]) * 3600 + int(end_time[1]) * 60 + int(end_time[2])
        # 前一天
        add_value(result_line, start_seconds, 24 * 3600-1)
        # 后一天
        add_value(result_line, 0, end_seconds)


# 计算每个主叫号码各时段通话时长比例
def main():
    data = DataLoader().load_data(sorted_by=Column.calling_nbr.value)  # 按主叫号码排序
    output = []
    result_line = [data[0][Column.calling_nbr.value], 0, 0, 0, 0, 0, 0, 0, 0]  # 当前处理行
    last_number = data[0][Column.calling_nbr.value]
    for line in tqdm(data):
        if line[Column.calling_nbr.value] == last_number:  # 通话记录中的主叫号码与上一条相同
            start_time = line[Column.start_time.value]
            end_time = line[Column.end_time.value]
            update_time_value(result_line, start_time, end_time)

        else:  # 通话记录中的主叫号码与上一条不同
            # 计算比例，然后添加到输出
            calc(result_line)
            output.append(result_line)
            last_number = line[Column.calling_nbr.value]
            result_line = [line[Column.calling_nbr.value], 0, 0, 0, 0, 0, 0, 0, 0]
            start_time = line[Column.start_time.value]
            end_time = line[Column.end_time.value]
            update_time_value(result_line, start_time, end_time)
    # 计算比例，然后添加到输出
    calc(result_line)
    output.append(result_line)
    DataWriter("percentage_in_segments.xlsx",
               ["主叫号码", "时间段1占比", "时间段2占比", "时间段3占比", "时间段4占比", "时间段5占比", "时间段6占比",
                "时间段7占比", "时间段8占比"]).write_data(output)


if __name__ == '__main__':
    main()
