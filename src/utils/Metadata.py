from enum import Enum


class TimeSegment(Enum):
    SEG_1 = [0, 3]  # 时间0:00-3:00
    SEG_2 = [3, 6]  # 时间3:00-6:00
    SEG_3 = [6, 9]  # 时间6:00-9:00
    SEG_4 = [9, 12]  # 时间9:00-12:00
    SEG_5 = [12, 15]  # 时间12:00-15:00
    SEG_6 = [15, 18]  # 时间15:00-18:00
    SEG_7 = [18, 21]  # 时间18:00-21:00
    SEG_8 = [21, 24]  # 时间21:00-24:00


class Column(Enum):
    day_id = 0
    calling_nbr = 1  # 主叫号码 全部为本运营商加密后的手机号码
    called_nbr = 2  # 被叫号码 g开头号码表示各运营商各城市固话号码，y开头号码表示异网手机号码，其它为本运营商手机号码
    calling_optr = 3  # 主叫号码运营商 1：电信；2：移动；3：联通；其它为不详
    called_optr = 4  # 被叫号码运营商 1：电信；2：移动；3：联通；其它为不详
    calling_city = 5  # 主叫号码归属地 主叫号码所归属的城市
    called_city = 6  # 被叫号码归属地 被叫号码所归属的城市
    calling_roam_city = 7  # 主叫号码漫游地 主叫号码所在的漫游城市，没有漫游时则为空
    called_roam_city = 8  # 被叫号码漫游地 被叫号码所在的漫游城市，没有漫游时则为空
    start_time = 9  # 通话开始时间 格式：13:44:25（时:分:秒）
    end_time = 10  # 通话结束时间 格式：13:44:25（时:分:秒）
    raw_dur = 11  # 通话时长 单位：秒
    call_type = 12  # 通话类型 1：市话；2：长途；3：漫游
    calling_cell = 13  # 主叫蜂窝号码 所在的基站蜂窝标识或为空


data_file_path="filter-data.txt"
