    
# import mysql.connector as mydb
import codecs
import random
import pymysql.cursors


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             database='test',
                             port = 3308,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

def bytes_to_int(bytes_val: bytes) -> int:
    return int.from_bytes(bytes_val, "big")


def int_to_bytes(int_val: int) -> bytes:
    return int(int_val).to_bytes((int(int_val).bit_length() + 7) // 8, "big")

def init_table():
    sql = "create table if not exists galaxy (no_of_atoms blob);"
    cursor.execute(sql)


def init_function():
    sql = """CREATE AGGREGATE FUNCTION big_average RETURNS STRING SONAME "big_average.so";"""
    cursor.execute(sql)


def drop_function():
    sql = """DROP FUNCTION big_average;"""
    cursor.execute(sql)


# drop test table
def drop_table():
    sql = """DROP TABLE galaxy;"""
    cursor.execute(sql)

def int_to_hex(val:int)->str:
    return val.to_bytes(((int.bit_length() + 7) // 8), "big").hex()

def test_big_average():
    input_range = 5

    vals = [random.randint(2**256, 2**512) for _ in range(input_range)]
    # vals = [25, 25, 25, 25, 25]
    # print(vals)
    sum = 0

    for v in vals:
        sum += v
        val_bytes = int_to_bytes(v)
        sql = f"""insert into galaxy values(%s);"""
        cursor.execute(sql, (val_bytes))
        connection.commit()

    sql = f"SELECT big_average(HEX(no_of_atoms)) FROM galaxy;"
    print(f"{sql}")
    cursor.execute(sql)
    result = cursor.fetchone()
    vals = []
    if isinstance(result, dict):
        for v in result.values():
            vals.append(v)

    avg_int = int(vals[0], 16)
    print("MySQL UDF AVG = ", avg_int)
    py_avg = sum//input_range
    print("Python AVG    = ", py_avg)
    assert avg_int == py_avg


   

init_table()
# init_function()
test_big_average()
# drop_function()
drop_table()
