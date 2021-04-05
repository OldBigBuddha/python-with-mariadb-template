import os

import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import CursorBase

try:
    DB_HOST = os.environ["MYSQL_HOST"]
    DB_USER = os.environ["MYSQL_USER"]
    DB_PASS = os.environ["MYSQL_PASSWORD"]
    DB_NAME = os.environ["MYSQL_DATABASE"]

    conn: MySQLConnection = mysql.connector.connect(
        host=DB_HOST,
        port=3306,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

    conn.ping(reconnect=True)
    print("Connect successfully." if conn.is_connected()
          else "Not connect to DB yet.")

    cursor: CursorBase = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS `test_table`;")
    cursor.execute(
        """
        create table if not exists `test_table` (
            `id` int auto_increment primary key,
            `content` varchar(2000) not null,
            `created_at` datetime not null default NOW()
        ) ENGINE=InnoDB default CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """
    )

    cursor.execute(
        """
        insert into test_table (content)
        values (
            'My First Task'
        );
        """
    )
    cursor.execute(
        """
        insert into test_table (content)
        values (
            'My Second Task'
        );
        """
    )
    conn.commit()

    cursor.execute(
        """
        SELECT *
        FROM test_table;
        """
    )

    for (id, content, created_by) in cursor.fetchall():
        print(f"ID: {id} / Content: {content} / Created by: {created_by}")

except mysql.connector.Error as err:
    print("VendorError:", err.errno)
    print("SQLState:", err.sqlstate)
    print("SQLException:", err.msg)

else:
    cursor.close()
    conn.close()
