from utils.DataLoader import DataLoader
from utils.Metadata import Column
from tqdm import tqdm



def main():
    data=DataLoader().load_data(sorted_by=Column.calling_nbr.value)  # 按主叫号码排序
    # 每个主叫号码是一个用户
    # 按主叫号码合并同一用户的通话记录，其余所有属性值全部按平均值处理



if __name__ == "__main__":
    main()
