# Brendon's solution

# import PostgreSQL databse adapter for the Python programming language
import psycopg2

# http://bleach.readthedocs.io/en/latest/, an HTML sanitizing library that
# escapes or strips markup and attributes
import bleach

def get_posts():
    # assign db to connection object
    db = psycopg2.connect("dbname=forum")
    # create cursor
    active_cursor = db.cursor()
    # create query
    query = "select content, time from posts order by id desc"
    # execute query
    active_cursor.execute(query)
    # store cursor query result in posts variable
    posts = active_cursor.fetchall()
    # close database connection
    db.close()
    # return posts
    return posts

def add_post(content):
    # clean input content with bleach (bleach does not prevent SQL injection or other errors)
    content = bleach.clean(content)
    # assign db to connection object
    db = psycopg2.connect("dbname=forum")
    # create cursor
    active_cursor = db.cursor()
    # create query and then execute query securely
    query = "insert into posts (content) values (%s)"
    active_cursor.execute(query, (content,))
    # commit changes
    db.commit()
    # close database connection (not executed?)
    db.close()

"""
# Database vulnerabilities
1. Check for apostrophies

2. Protect against SQL injection
'); delete from posts; --

3. Protect against script injection
<script>
setTimeout(function() {
    var tt = document.getElementById('content');
    tt.value = "<h2 style='color: #FF6699; font-family: Comic Sans MS'>Spam, spam, spam, spam,<br>Wonderful spam, glorious spam!</h2>";
    tt.form.submit();
}, 2500);
</script>
"""

'''
# Original "backend" code without database
# "Database code" for the DB Forum.

import datetime

POSTS = [("This is the first post.", datetime.datetime.now())]

def get_posts():
  """Return all posts from the 'database', most recent first."""
  return reversed(POSTS)

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  POSTS.append((content, datetime.datetime.now()))
'''
