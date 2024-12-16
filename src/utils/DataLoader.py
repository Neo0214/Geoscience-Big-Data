import os

from .Metadata import data_file_path
from tqdm import tqdm

class DataLoader:
    def __init__(self):
        self.data_path = os.getcwd().split("src")[0]+data_file_path
        self.data = []

    def load_data(self,sorted_by:int=None)->list:
        with open(self.data_path, "r") as f:
            for line in tqdm(f):
                self.data.append(line.strip().split())
        if sorted_by is None:
            return self.data
        return sorted(self.data,key=lambda x:x[sorted_by])
