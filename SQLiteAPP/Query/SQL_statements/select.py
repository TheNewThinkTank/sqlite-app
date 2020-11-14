
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
