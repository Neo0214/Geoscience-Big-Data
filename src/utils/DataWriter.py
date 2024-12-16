import pandas as pd
import os


class DataWriter:
    def __init__(self, target: str, column_names: list):
        self.column_names = column_names
        self.path = os.getcwd().split("src")[0] + "\\result\\" + target

    def write_data(self, data: list):
        # 组合格式
        dt: dict = {self.column_names[i]:
                        [data[j][i] for j in range(len(data))]
                    for i in range(len(self.column_names))}
        df: pd.DataFrame = pd.DataFrame(dt)
        df.to_excel(self.path, index=False)
