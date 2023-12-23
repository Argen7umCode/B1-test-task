import pandas as pd
import re
import itertools 

from typing import List, Tuple


class Parser:
    """
        Класс который обрабатывает полученный эксель файл и возвращает данные 
    """
    def __init__(self) -> None:
        self.r = re.compile('КЛАСС  \d|ПО КЛАССУ')
        self.re = re.compile('КЛАСС  \d')

    @staticmethod
    def _read_file(path: str) -> pd.DataFrame:
        # Читает файл
        return pd.read_excel(path, engine='openpyxl')

    def _get_split_indexes(self, df: pd.DataFrame) -> List[Tuple[int, int]]:
        # Получает индексы начала и конца класса и возвращает их
        return list(itertools.batched(df.iloc[:, 0][df.iloc[:, 0].apply(lambda x: 
                                                                        bool(self.r.match(str(x))))].index, 2))

    @staticmethod
    def _clear_df(df: pd.DataFrame) -> pd.DataFrame:
        # Очищает датасет
        df = df.iloc[:, :-2]
        df = df.drop(df.iloc[:, 0][df.iloc[:, 0].apply(lambda a: len(str(a)) == 2)].index).reset_index(drop=True) 
        return df

    @staticmethod
    def _get_chank_data(df: pd.DataFrame, st_index: int, fin_index: int) -> List[pd.DataFrame]:
        # Возвращает часть даных из датасета по индексам начала и конца
        return df.iloc[st_index+1:fin_index].set_axis(['unid', 'active', 'passive', 'debit', 'credit'], axis=1)\
                                            .reset_index(drop=True)

    def _get_classes_from_data(self, df: pd.DataFrame) -> List[str]:
        # Получает имена классов в датасете
        classes = df.iloc[:, 0][df.iloc[:, 0].apply(lambda x: bool(self.re.match(str(x))))]\
                                             .apply(lambda x: re.sub(self.re, '', x).strip())\
                                             .to_list()
        return classes

    def get_classes_from_excel_file(self, path: str) -> dict:
        # Обрабатывает весь датасет и возвращает классы и участки данных этих классов
        df = self._read_file(path)
        cl_df = self._clear_df(df)
        indxs = self._get_split_indexes(cl_df)
        classes = self._get_classes_from_data(df)

        dfs = {class_ : self._get_chank_data(cl_df, st, fin) 
                    for class_, (st, fin) in zip(classes, indxs)}
        return dfs
    
