from src.utils.DataLoader import DataLoader
from src.utils.Metadata import Column
from src.utils.DataWriter import DataWriter
import os
from tqdm import tqdm


# 计算每个主叫号码的日均通话次数
def main():
    data = DataLoader().load_data(sorted_by=Column.calling_nbr.value)  # 按主叫号码排序
    output = [[data[0][Column.calling_nbr.value], 0]]  # 元素: [主叫号码，日均通话次数]
    last_calling_nbr = data[0][Column.calling_nbr.value]
    for line in tqdm(data):
        if line[Column.calling_nbr.value] == last_calling_nbr:  # 通话记录中的主叫号码与上一条相同
            output[-1][1] += 1
        else:  # 通话记录中的主叫号码与上一条不同
            output.append([line[Column.calling_nbr.value], 1])
            last_calling_nbr = line[Column.calling_nbr.value]
    output = [[output[i][0], output[i][1] / 29] for i in range(len(output))]  # 计算日均通话次数
    DataWriter("call_per_day.xlsx", ["主叫号码", ", 每日平均通话次数"]).write_data(output)


if __name__ == "__main__":
    main()
