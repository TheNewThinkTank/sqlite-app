#!/usr/bin/env python
# sqlite_app.py
__version__ = '0.1.0'

from pprint import pprint as pp
import sqlite3
from sqlite3 import Error


def create_connection(path):
    """."""
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    """."""
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    """."""
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


create_tables = {"create_users_table": """
                    CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    nationality TEXT
                    );
                    """,
                 "create_posts_table": """
                    CREATE TABLE IF NOT EXISTS posts(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                    );
                    """,
                 "create_comments_table": """
                    CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    post_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (post_id) REFERENCES posts (id)
                    );
                    """,
                 "create_likes_table": """
                    CREATE TABLE IF NOT EXISTS likes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    post_id integer NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (post_id) REFERENCES posts (id)
                    );
                    """
                 }

insert_data = {"create_users": """
                  INSERT INTO
                  users (name, age, gender, nationality)
                  VALUES
                  ('James', 25, 'male', 'USA'),
                  ('Leila', 32, 'female', 'France'),
                  ('Brigitte', 35, 'female', 'England'),
                  ('Mike', 40, 'male', 'Denmark'),
                  ('Elizabeth', 21, 'female', 'Canada');
                  """,
               "create_posts": """
                INSERT INTO
                posts (title, description, user_id)
                VALUES
                ("Happy", "I am feeling very happy today", 1),
                ("Hot Weather", "The weather is very hot today", 2),
                ("Help", "I need some help with my work", 2),
                ("Great News", "I am getting married", 1),
                ("Interesting Game", "It was a fantastic game of tennis", 5),
                ("Party", "Anyone up for a late-night party today?", 3);
                """,
               "create_comments": """
                INSERT INTO
                comments (text, user_id, post_id)
                VALUES
                ('Count me in', 1, 6),
                ('What sort of help?', 5, 3),
                ('Congrats buddy', 2, 4),
                ('I was rooting for Nadal though', 4, 5),
                ('Help with your thesis?', 2, 3),
                ('Many congratulations', 5, 4);
                """,
               "create_likes": """
                    INSERT INTO
                    likes (user_id, post_id)
                    VALUES
                    (1, 6),
                    (2, 3),
                    (1, 5),
                    (5, 4),
                    (2, 4),
                    (4, 2),
                    (3, 6);
                    """
               }

select_data = {"select_users": "SELECT * from users",
               "select_posts": "SELECT * FROM posts",
               "select_users_posts": """
                  SELECT
                  users.id,
                  users.name,
                  posts.description
                  FROM
                  posts
                  INNER JOIN users ON users.id = posts.user_id
                  """,
               "select_posts_comments_users": """
                  SELECT
                  posts.description as post,
                  text as comment,
                  name
                  FROM
                  posts
                  INNER JOIN comments ON posts.id = comments.post_id
                  INNER JOIN users ON users.id = comments.user_id
                  """,
               "select_post_likes": """
                  SELECT
                  description as Post,
                  COUNT(likes.id) as Likes
                  FROM
                  likes,
                  posts
                  WHERE 1=1
                  AND posts.id = likes.post_id
                  -- AND Likes > 1
                  GROUP BY
                  likes.post_id
                  """,
               "select_post_description": """
                  SELECT description FROM posts WHERE id = 2"""
               }

update_post_description = """
UPDATE
posts
SET
description = "The weather has become pleasant now"
WHERE
id = 2
"""

delete_comment = "DELETE FROM comments WHERE id = 5"


def create_tables(connection):
    """."""
    execute_query(connection, create_tables["create_users_table"])
    execute_query(connection, create_tables["create_posts_table"])
    execute_query(connection, create_tables["create_comments_table"])
    execute_query(connection, create_tables["create_likes_table"])


def insert_records(connection):
    """."""
    execute_query(connection, insert_data["create_users"])
    execute_query(connection, insert_data["create_posts"])
    execute_query(connection, insert_data["create_comments"])
    execute_query(connection, insert_data["create_likes"])


def select_records(connection):
    """Various select statements."""
    users = execute_read_query(connection, select_data["select_users"])
    pp(users)
    posts = execute_read_query(connection, select_data["select_posts"])
    pp(posts)

    # Join tables
    users_posts = execute_read_query(
        connection, select_data["select_users_posts"])
    pp(users_posts)

    posts_comments_users = execute_read_query(
        connection, select_data["select_posts_comments_users"]
    )
    pp(posts_comments_users)

    # Return column names
    cursor = connection.cursor()
    cursor.execute(select_data["select_posts_comments_users"])
    cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    pp(column_names)

    # Posts with total number of likes
    post_likes = execute_read_query(
        connection, select_data["select_post_likes"]
        )
    pp(post_likes)


def update_records(connection):
    """Show current post description, then update it."""
    post_description = execute_read_query(
        connection, select_data["select_post_description"]
    )
    pp(post_description)
    execute_query(connection, update_post_description)


def delete_records(connection):
    """Delete comment record."""
    execute_query(connection, delete_comment)


def main():
    """Driver function."""
    connection = create_connection(r"Desktop\Python\sm_app.sqlite")

    db_choice = input("""Do you want to create tables, insert,
                         select, update or delete records (c/i/s/u/d)?"""
                      ).replace("\n", "")

    db_actions = {"c": "create_tables(connection)",
                  "i": "insert_records(connection)",
                  "s": "select_records(connection)",
                  "u": "update_records(connection)",
                  "d": "delete_records(connection)"
    }

    exec(db_actions.get(db_choice))


if __name__ == '__main__':
    main()
