import pandas as pd
import re
import itertools 

from typing import List, Tuple


class Parser:

    def __init__(self) -> None:
        self.r = re.compile('КЛАСС  \d|ПО КЛАССУ')

    @staticmethod
    def _read_file(path: str) -> pd.DataFrame:
        return pd.read_excel(path, engine='openpyxl')

    def _get_split_indexes(self, df: pd.DataFrame) -> List[Tuple[int, int]]:
        return list(itertools.batched(df.iloc[:, 0][df.iloc[:, 0].apply(lambda x: bool(self.r.match(str(x))))].index, 2))

    @staticmethod
    def _clear_df(df: pd.DataFrame) -> pd.DataFrame:
        df = df.iloc[:, :-2]
        df = df.drop(df.iloc[:, 0][df.iloc[:, 0].apply(lambda a: len(str(a)) == 2)].index).reset_index(drop=True) 
        return df

    @staticmethod
    def _get_chank_data(df: pd.DataFrame, st_index: int, fin_index: int) -> List[pd.DataFrame]:
        return df.iloc[st_index+1:fin_index].set_axis(['unid', 'active', 'passive', 'debit', 'credit'], axis=1)

    def get_classes_from_excel_file(self, path: str) -> List[pd.DataFrame]:
        df = self._read_file(path)
        cl_df = self._clear_df(df)
        indxs = self._get_split_indexes(cl_df)
        return [self._get_chank_data(cl_df, st, fin) for st, fin in indxs]
    