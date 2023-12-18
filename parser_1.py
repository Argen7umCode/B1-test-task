import pandas as pd
import re
import itertools 

from typing import List, Tuple




class Parser:

    def __init__(self) -> None:
        self.r = re.compile('КЛАСС  \d|ПО КЛАССУ')
        self.re = re.compile('КЛАСС  \d')

    @staticmethod
    def _read_file(path: str) -> pd.DataFrame:
        return pd.read_excel(path, engine='openpyxl')

    def _get_split_indexes(self, df: pd.DataFrame) -> List[Tuple[int, int]]:
        return list(itertools.batched(df.iloc[:, 0][df.iloc[:, 0].apply(lambda x: 
                                                                        bool(self.r.match(str(x))))].index, 2))

    @staticmethod
    def _clear_df(df: pd.DataFrame) -> pd.DataFrame:
        df = df.iloc[:, :-2]
        df = df.drop(df.iloc[:, 0][df.iloc[:, 0].apply(lambda a: len(str(a)) == 2)].index).reset_index(drop=True) 
        return df

    @staticmethod
    def _get_chank_data(df: pd.DataFrame, st_index: int, fin_index: int) -> List[pd.DataFrame]:
        return df.iloc[st_index+1:fin_index].set_axis(['unid', 'active', 'passive', 'debit', 'credit'], axis=1).reset_index(drop=True)

    def _get_classes_from_data(self, df: pd.DataFrame) -> List[str]:
        classes = df.iloc[:, 0][df.iloc[:, 0].apply(lambda x: bool(self.re.match(str(x))))]\
                                             .apply(lambda x: re.sub(self.re, '', x).strip())\
                                             .to_list()
        return classes

    def get_classes_from_excel_file(self, path: str) -> dict:
        df = self._read_file(path)
        cl_df = self._clear_df(df)
        indxs = self._get_split_indexes(cl_df)
        classes = self._get_classes_from_data(df)

        dfs = {class_ : self._get_chank_data(cl_df, st, fin) 
                    for class_, (st, fin) in zip(classes, indxs)}
        return dfs
    

class Groupper(Parser):

    @staticmethod
    def _get_output_balance(df: pd.DataFrame) -> pd.DataFrame:
        df['output_active'] = df['active'] + df['debit'] - df['credit']
        df.loc[df['active']  == 0, 'output_active'] = 0

        df['output_passive'] = df['passive'] - df['debit'] + df['credit']
        df.loc[df['passive']  == 0, 'output_passive'] = 0
        return df.astype('float128')
    
    def add_group_result(self, df: pd.DataFrame) -> pd.DataFrame:
        conc_df = pd.DataFrame()
        for id, gr_df in df.groupby(df.unid.apply(lambda a: int(a) // 100)):
            res = gr_df.sum(axis=0)
            res.unid = id
            conc_df = pd.concat([conc_df, gr_df, pd.DataFrame(res).T]).reset_index(drop=True)
        return conc_df
    
    def add_class_result(self, df: pd.DataFrame) -> pd.DataFrame:
        result = pd.DataFrame(df[df.unid > 99].sum(axis=0)).T
        result.unid = "ИТОГО ЗА КЛАСС"
        return pd.concat([df, result]).reset_index(drop=True)
    
    def add_total_result(self, dfs: List[pd.DataFrame]) -> pd.DataFrame:
        df = pd.concat([self.add_class_result(
                            self.add_group_result(
                                self._get_output_balance(df_)
                                )
                            ) 
                        for df_ in dfs])
        result = pd.DataFrame(df[df.unid == 'ИТОГО ЗА КЛАСС'].sum(axis=0)).T
        result.unid = "ИТОГО"
        return pd.concat([df, result]).reset_index(drop=True)
    
    def get_grouped_data(self, path: str) -> pd.DataFrame:
        dfs = self.get_classes_from_excel_file(path)
        return self.add_total_result(dfs)