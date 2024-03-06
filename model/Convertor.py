import os
from typing import Tuple

import pandas as pd
from img2table.document import Image
from img2table.ocr import TesseractOCR


class Convertor():
    def __init__(self, path: str):
        self.path = path

    def __column_to_array(self, arr: list):
        result = []
        for i in range(len(arr)):
            temp = arr[i]
            try:
                temp = temp.split('\n')
                float_array = [float(string.replace(',', '.')) for string in temp]
                temp = float_array
            except:
                pass
            result += temp
        return result

    def __normalize_columns(self, dic: dict) -> Tuple:
        max_length = max(map(len, dic.values()))
        flag = True
        for i in dic.keys():
            for j in range(0, abs(len(dic[i]) - max_length)):
                dic[i].append(0)
                flag = False
        return dic, flag

    def to_csv(self) -> bool:
        image = Image(self.path)
        ocr = TesseractOCR(lang="eng")
        imgage_tables = image.extract_tables(ocr=ocr)
        dic = {}
        for i in imgage_tables[0].df:
            dic[i] = self.__column_to_array(imgage_tables[0].df[i].tolist())
        dic, flag = self.__normalize_columns(dic)
        df = pd.DataFrame(dic)
        df.to_csv(self.path.replace('.jpg', '.csv'), index=False)
        return True

    def remove_file(self):
        os.remove(self.path)
        os.remove(self.path.replace('.jpg', '.csv'))
