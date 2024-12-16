from utils.DataLoader import DataLoader
from utils.Metadata import Column


def check_time(time_list):
    # 检查是否是 xx:xx:xx 格式
    for time in time_list:
        if len(time) != 8:
            print("时间格式错误")
            return
        if time[2] != ":" or time[5] != ":":
            print("时间格式错误")
            return
        if not time[0:2].isdigit() or not time[3:5].isdigit() or not time[6:8].isdigit():
            print("时间格式错误")
            return
        if int(time[0:2]) > 24 or int(time[3:5]) > 60 or int(time[6:8]) > 60:
            print("时间格式错误")
            return


def main():
    loader = DataLoader()
    data = loader.load_data()
    call_start_time=[line[Column.start_time.value] for line in data]
    call_end_time=[line[Column.end_time.value] for line in data]
    check_time(call_end_time)



if __name__ == "__main__":
    main()
