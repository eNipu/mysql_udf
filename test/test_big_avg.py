    
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
# create test table
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

    vals = [random.randint(2**31, 2**64) for _ in range(input_range)]
    # vals = [25, 25, 25, 25, 25]
    print(vals)
    sum = 0

    for v in vals:
        sum += v
        hs = int_to_bytes(v)
        # print(f'ctxt:{hs}')
        # iv = int.from_bytes(hs, "big")
        # print("int=", iv)
        # hs = hex(v)

        sql = f"""insert into galaxy values(%s);"""
        print(f"sql to insert:: {sql}")
        cursor.execute(sql, (hs))
        connection.commit()

    sql = f"SELECT big_average(HEX(no_of_atoms)) FROM galaxy;"
    print(f"{sql}")
    cursor.execute(sql)
    result = cursor.fetchone()
    vals = []
    if isinstance(result, dict):
        for v in result.values():
            vals.append(v)

    print(vals)
    val_s = int(vals[0], 16)
    print(val_s)
    print("Python AVG = ", sum)


   

init_table()
# init_function()
test_big_average()
# drop_function()
drop_table()
