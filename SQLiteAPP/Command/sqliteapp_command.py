"""Set up SQLite database connection,
create tables,
load data into tables,
update or delete data.
"""

# from pprint import pprint as pp
import sqlite3
from sqlite3 import Error

from SQL_statements.create import create_tables
from SQL_statements.delete import delete_comment
from SQL_statements.insert import insert_data
from SQL_statements.update import update_post_description


def create_connection(path):
    """_summary_

    :param path: _description_
    :type path: _type_
    :return: _description_
    :rtype: _type_
    """

    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query):
    """_summary_

    :param connection: _description_
    :type connection: _type_
    :param query: _description_
    :type query: _type_
    """

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def create_table(connection):
    """_summary_

    :param connection: _description_
    :type connection: _type_
    """

    execute_query(connection, create_tables["create_users_table"])
    execute_query(connection, create_tables["create_posts_table"])
    execute_query(connection, create_tables["create_comments_table"])
    execute_query(connection, create_tables["create_likes_table"])


def insert_records(connection):
    """_summary_

    :param connection: _description_
    :type connection: _type_
    """

    execute_query(connection, insert_data["create_users"])
    execute_query(connection, insert_data["create_posts"])
    execute_query(connection, insert_data["create_comments"])
    execute_query(connection, insert_data["create_likes"])


def update_records(connection):
    """Update post description.

    :param connection: _description_
    :type connection: _type_
    """

    execute_query(connection, update_post_description)


def delete_records(connection):
    """Delete comment record.

    :param connection: _description_
    :type connection: _type_
    """

    execute_query(connection, delete_comment)


def main():
    """Driver function."""

    connection = create_connection(r"Desktop\\Python\sm_app.sqlite")

    db_choice = input("""Do you want to create tables, insert,
                         update or delete records (c/i/s/u/d)?"""
                      ).replace("\n", "")

    db_actions = {"c": "create_table(connection)",
                  "i": "insert_records(connection)",
                  "u": "update_records(connection)",
                  "d": "delete_records(connection)"
    }

    exec(db_actions.get(db_choice))


if __name__ == '__main__':
    main()
