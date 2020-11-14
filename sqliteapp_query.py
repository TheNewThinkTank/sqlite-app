"""
Query SQLite database
"""

from pprint import pprint as pp
import sqlite3
from sqlite3 import Error

from sqliteapp_command import create_connection

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


def main():
    """Driver function."""
    connection = create_connection(r"Desktop\Python\sm_app.sqlite")

    post_description = execute_read_query(
        connection, select_data["select_post_description"]
    )
    pp(post_description)


if __name__ == '__main__':
    main()
