from random import randint, random, randrange, choices
from datetime import datetime, timedelta
from string import ascii_letters
from re import sub
from typing import Optional, List, Any, Callable
import pandas as pd
import sqlite3


alphabet_kir = ''.join(map(chr, list(range(ord('а'), ord('я'))) + \
                                list(range(ord('А'), ord('Я')))))
alphabet_lat = ascii_letters


def random_date() -> datetime:
    delta = timedelta(seconds = 5 * 365 * 24 * 3600)
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return datetime.now() - timedelta(seconds = random_second)


def random_float() -> float:
    return round(random() * 20, 8)


def random_int() -> int:
    return randint(1, 100_000_000)


def random_string(alphabet: str, lenght: int) -> str:
    return ''.join(choices(alphabet, k=lenght))


def get_random_string() -> str:
    return '||'.join([
        random_date().strftime('%d.%m.%Y'), random_string(alphabet_lat, 10), 
        random_string(alphabet_kir, 10), str(random_int()), str(random_float())
    ]) + '||'


def get_n_random_strings(num: int) -> str:
    return '\n'.join(get_random_string() for _ in range(num))


def save_random_strings(path: str) -> None:
    data = get_n_random_strings(100_000)
    with open(path, 'w') as file:
        file.write(data)


def read_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()


def remove_pattern(data: str, pattern: str) -> [str, int]:
    cleaned_data = sub(pattern, '', data)
    count = (len(data) - len(cleaned_data)) // len(pattern)
    return cleaned_data, count


def concat_files(file_path: str,
                 pathes: List[str], 
                 pattern_to_remove: Optional[str] = None) -> str:
    with open(file_path, "a") as file:
        for path in pathes:
            data = read_file(path) + '\n'
            if pattern_to_remove:
                data, count = remove_pattern(data, pattern_to_remove)
                print(f'Removed: {count}')
            file.write(data)


def split_by_rows(data: str) -> List[str]:
    return data.split('\n')


def split_row_by_spliter(row: str, sp: str = '||') -> List[str]:
    return row[:-2].split(sp)


def split_data(data: str, sp: str = '||') -> List[List[str]]:
    return [split_row_by_spliter(row, sp) for row in split_by_rows(data)]


def convert_field_to_datatype(item: str, instance: Callable) -> Any:
    try:
        item = instance(item)
    except TypeError:
        print(f"Can't convert {item} to {instance}. {item} is still str-type")
    return item


def convert_row_to_datatypes(row: List[str],
                               datatypes: List[Callable]) -> List[Any]:
    return tuple([convert_field_to_datatype(row, instance) for row, instance in zip(row, datatypes)])


def convert_data_to_datatypes(data: List[List[str]],
                                datatypes: List[Callable]) -> List[List[Any]]:
    return [convert_row_to_datatypes(row, datatypes) for row in data]


def create_table():
    with sqlite3.connect('my_db.db') as con:
        cursor = con.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data (
                date TEXT NOT NULL,
                lat_data TEXT NOT NULL,
                kir_data TEXT NOT NULL,
                int_num INTEGER NOT NULL,
                float_num REAL NOT NULL
            )
        ''')


def insert_into_db(data: str, db_path: str):
    datatypes = [str, str, str, int, float]
    data = split_data(data)[:-1]
    conv_data = convert_data_to_datatypes(data, datatypes)
    df = pd.DataFrame(conv_data, 
                      columns=['date', 'lat_data', 'kir_data', 'int_num', 'float_num'])
    with sqlite3.connect(db_path) as connection:
        inserted = df.to_sql("data", con=connection, if_exists="append", index=False)
        connection.commit()
        print(f'Inserted: {inserted}')


def get_stat_data(db_path):
    with sqlite3.connect(db_path) as connection:
        cur = connection.cursor()
        median = cur.execute(
            """SELECT float_num
               FROM data
               ORDER BY float_num
               LIMIT 1
               OFFSET (SELECT COUNT(*)
               FROM data) / 2""").fetchone()[0]
        sum_ = cur.execute("""SELECT SUM(int_num) FROM data""").fetchone()[0]
        return sum_, median
    

if __name__ == '__main__':
    pathes = [f'data/data_{i}.txt' for i in range(100)]

    for path in pathes:
        save_random_strings(path)

    concat_files('file.txt', pathes)
    data = read_file('file.txt')
    create_table()
    insert_into_db(data, 'my_db.db')
    get_stat_data('my_db.db')