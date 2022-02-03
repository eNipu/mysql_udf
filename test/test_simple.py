import mysql.connector as mydb
import random
import base64
conn = mydb.connect(
    host='127.0.0.1',
    port='3306',
    user='root',
    password='password',
    database='test'
)

cur = conn.cursor()


def init_table():
    cur.execute(
        """
        create table if not exists product (id int, val blob);
        """
    )

    cur.execute(
        """
        insert into product values (1, 'aafa'); 
        """
    )

    cur.execute(
        """
        select * from product;
        """
    )
    for i in cur:
        print(f"{i}")


def init_function():

    cur.execute(
        """
        CREATE FUNCTION big_average RETURNS STRING SONAME "big_average.so";
        """
    )


def drop_function():
    cur.execute(
        """
        DROP FUNCTION big_average;
        """
    )
#drop test table


def drop_table():
    cur.execute(
        """
        DROP TABLE product;
        """
    )


def test_function():
    cur.execute(
        """
        select big_average(hex(val)) from product;
        """
    )
    for i in cur:
        print(f"{i}")


def test_function_bignum():
    a = random.randint(2**255, 2**256)
    b = random.randint(2**255, 2**256)
    p = random.randint(2**255, 2**256)
    a_str = hex(a)
    b_str = hex(b)
    # base64 string (not byte string)
    p_base64 = base64.b64encode(hex(p).encode()).decode()

    print("""
        select big_average('{}','{}','{}');
        """.format(a_str, b_str, p_base64)
          )

    cur.execute(
        """
        select big_average('{}','{}','{}');
        """.format(a_str, b_str, p_base64)
    )
    for i in cur:
        print("mysql_udf:"+f"{i[0].decode()}")

    print("python   :"+format((a*b) % (p*p), 'x'))


init_table()
init_function()
test_function_bignum()
drop_function()
drop_table()
