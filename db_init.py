from decimal import Decimal
from datetime import date
from datetime import datetime


import json

from pony.orm.core import *

db = Database()

#delete from usermention; delete from hashtag; delete from url; delete from tweet; delete from user;
#drop table usermention; drop table  hashtag; drop table  url; drop table  tweet; drop table  user;

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
    in_reply_to_user_id = Optional(int, size=64)
    created_at = Optional(datetime)
    favourite_count = Optional(int)
    truncated = Optional(bool)
    contributors = Optional(str, nullable=True)
    retweet_count = Optional(int)
    text = Required(LongUnicode)
    text_full = Optional(LongUnicode, nullable=True)
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
    hashtags = Set('Hashtag')
    urls = Set('Url')
    user_mentions = Set('UserMention')
    place = Optional('Place')
    retweet_from_tweet_id = Optional(int, size=64)


class Hashtag(db.Entity):
    id = PrimaryKey(int, auto=True)
    text = Required(unicode)
    tweet = Required(Tweet)

class Url(db.Entity):
    id = PrimaryKey(int, auto=True)
    expanded_url = Required(unicode)
    url = Required(unicode)
    display = Required(unicode)
    tweet = Required(Tweet)

class UserMention(db.Entity):
    _table_ = "user_mention"
    id = PrimaryKey(int, auto=True)
    tweet = Required(Tweet)
    id_user = Required(int, size=64)
    name = Optional(unicode)
    screen_name = Optional(unicode)

class Place(db.Entity):
    id = PrimaryKey(int, auto=True)
    tweet = Required(Tweet)
    full_name = Optional(unicode)
    name = Optional(unicode)
    place_type = Optional(unicode)
    country = Optional(unicode)
    country_code = Optional(unicode)
    

sql_debug(True)  # Output all SQL queries to stdout



params = dict(
    #sqlite=dict(provider='sqlite', filename='university1.sqlite', create_db=True),
    mysql=dict(provider='mysql', host="localhost", user="twitter_user", passwd="twitter_pass", db="twitter")
    #postgres=dict(provider='postgres', user='pony', password='twitter_user', host='localhost', database='twitter'),
    #oracle=dict(provider='oracle', user='c##pony', password='pony', dsn='localhost/orcl')
)
db.bind(**params['mysql'], charset='utf8mb4', use_unicode=True)


if __name__ == '__main__':
    print("GERANDO TABELAS....")
    db.generate_mapping(create_tables=True)
    with db_session:
        db.execute("SET NAMES utf8mb4;")
    #    db.execute("ALTER DATABASE twitter CHARACTER SET = utf8mb4;")
  
    
else:
    db.generate_mapping(create_tables=False)
    with db_session:
        db.execute("SET NAMES utf8mb4;")









