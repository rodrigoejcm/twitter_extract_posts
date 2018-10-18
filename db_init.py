from decimal import Decimal
from datetime import date
from datetime import datetime


import json

from pony.orm.core import *

db = Database()

class User(db.Entity):
    id = PrimaryKey(int, size=64)
    id_str = Required(str, unique=True)
    screen_name = Optional(str,nullable=True)
    created_at = Optional(datetime)
    is_translator = Optional(bool, nullable=True)
    name = Optional(str,nullable=True)
    description = Optional(str, nullable=True)
    statuses_count = Optional(int)
    friends_count = Optional(int)
    followers_count = Optional(int)
    verified = Optional(bool)
    location = Optional(str, nullable=True)
    geo_enabled = Optional(bool)
    protected = Optional(bool)
    lang = Optional(str, nullable=True)
    tweets = Set("Tweet")

class Tweet(db.Entity):
    id = PrimaryKey(int, size=64)
    id_str = Required(str, unique=True)
    in_reply_to_user_id = Optional(int)
    created_at = Optional(datetime)
    favourite_count = Optional(int)
    truncated = Optional(bool)
    contributors = Optional(str, nullable=True)
    retweet_count = Optional(int)
    text = Required(str)
    text_full = Optional(str, nullable=True)
    in_reply_to_status_id = Optional(int, size=64)
    filter_level = Optional(str, nullable=True)
    quote_count = Optional(int)
    geo = Optional(str, nullable=True)
    source = Optional(str, nullable=True)
    #place = Optional(str, nullable=True)
    possibly_sensitive = Optional(bool)
    in_reply_to_screen_name = Optional(str, nullable=True)
    is_quoted_status = Optional(bool)
    coordinates = Optional(str, nullable=True)
    reply_count = Optional(int)
    lang = Optional(str, nullable=True)
    user = Required(User)


class Student(db.Entity):
    # _table_ = "public", "Students"  # Schema support
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    dob = Required(date)
    tel = Optional(str)
    picture = Optional(buffer, lazy=True)
    gpa = Required(float, default=0)
    #group = Required(Group)

sql_debug(True)  # Output all SQL queries to stdout



params = dict(
    #sqlite=dict(provider='sqlite', filename='university1.sqlite', create_db=True),
    mysql=dict(provider='mysql', host="localhost", user="twitter_user", passwd="twitter_pass", db="twitter")
    #postgres=dict(provider='postgres', user='pony', password='twitter_user', host='localhost', database='twitter'),
    #oracle=dict(provider='oracle', user='c##pony', password='pony', dsn='localhost/orcl')
)
db.bind(**params['mysql'])


if __name__ == '__main__':
    print("GERANDO TABELAS....")
    db.generate_mapping(create_tables=True)
    #with db_session:
    #    db.execute(" ALTER TABLE user MODIFY COLUMN description VARCHAR(500) CHARACTER SET utf8 COLLATE utf8_general_ci;")
    #    db.execute(" ALTER TABLE user MODIFY location VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci;")
else:
    db.generate_mapping(create_tables=False)









