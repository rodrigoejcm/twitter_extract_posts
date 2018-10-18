import json
import db_init
import datetime
from pony.orm import *
from dateutil import parser


with open('/home/rodrigo/Projects/twitter_test_birdy_lib/twitter_ss.json', encoding='utf-8') as f:
    tweet_json = json.load(f)

@db_session
def save_data(json_data):

    
    id_user = json_data['user']['id']
    
    if not db_init.User.exists(id=id_user):
        description = json_data['user']['description'] if 'description' in json_data['user'] else None 
        if description : description = str(description.encode('unicode-escape')) 
        followers_count = json_data['user']['followers_count'] if 'followers_count' in json_data['user'] else None
        friends_count = json_data['user']['friends_count'] if 'friends_count' in json_data['user'] else None
        id_str_user = json_data['user']['id_str'] if 'id_str' in json_data['user'] else None 
        screen_name = json_data['user']['screen_name'] if 'screen_name' in json_data['user'] else None  
        created_at = parser.parse(json_data['user']['created_at']) if 'created_at' in json_data['user'] else None 
        is_translator = json_data['user']['is_translator'] if 'is_translator' in json_data['user'] else False 
        name = str(json_data['user']['name'].encode('unicode-escape')) if 'name' in json_data['user'] else None
        statuses_count = json_data['user']['statuses_count'] if 'statuses_count' in json_data['user'] else None
        verified = json_data['user']['verified'] if 'verified' in json_data['user'] else False
        location = str(json_data['user']['location'].encode('unicode-escape')) if json_data['user']['location'] else None
        geo_enabled = json_data['user']['geo_enabled'] if 'geo_enabled' in json_data['user'] else False
        protected = json_data['user']['protected'] if 'protected' in json_data['user'] else False
        lang = json_data['user']['lang'] if 'lang' in json_data['user'] else None
        
        

        user = db_init.User(
            id=id_user,
            description = description,
            followers_count = followers_count,
            friends_count = friends_count,
            id_str = id_str_user,
            screen_name = screen_name,
            created_at = created_at,
            is_translator = is_translator,
            name = name,
            statuses_count = statuses_count,
            verified = verified,
            location = location,
            geo_enabled = geo_enabled,
            protected = protected,
            lang = lang
        )
    else:
        user = db_init.User[id_user]



    #### TESTAR COM A API DIRETO COM OS VALORES PARA VER ESSA QUESTAO DO ENCODE.
    ### DESFAZER OS ENCODES EM TWEET e USER




    #tweet
    id = json_data['id']

    if not db_init.Tweet.exists(id=id): 
        id_str = json_data['id_str']
        in_reply_to_user_id = json_data['in_reply_to_user_id'] if 'in_reply_to_user_id' in json_data else None 
        created_at = parser.parse(json_data['created_at'])
        favourite_count = json_data['favourite_count'] if 'favourite_count' in json_data else None 
        truncated = json_data['truncated']
        #text_full = 
        #text_full = Optional(str, nullable=True)
        text = str(json_data['text'].encode('unicode-escape'))
        contributors = json_data['contributors'] if 'contributors' in json_data else None 
        retweet_count = json_data['retweet_count'] if 'retweet_count' in json_data else None 
        in_reply_to_status_id = json_data['in_reply_to_status_id'] if 'in_reply_to_status_id' in json_data else None 
        filter_level = json_data['filter_level'] if 'filter_level' in json_data else None 
        quote_count = json_data['quote_count'] if 'quote_count' in json_data else None 
        geo = json_data['geo'] if 'geo' in json_data else None 
        source = json_data['source'] if 'source' in json_data else None 
        #place = json_data['place'] if 'place' in json_data else None 
        possibly_sensitive = json_data['possibly_sensitive'] if 'possibly_sensitive' in json_data else False 
        in_reply_to_screen_name = json_data['in_reply_to_screen_name'] if 'in_reply_to_screen_name' in json_data else None 
        is_quoted_status = json_data['is_quoted_status'] if 'is_quoted_status' in json_data else False 
        coordinates = json_data['coordinates'] if 'coordinates' in json_data else None 
        reply_count = json_data['reply_count'] if 'reply_count' in json_data else None 
        lang =  json_data['lang'] if 'lang' in json_data else None 

        tweet = db_init.Tweet(
            user = user,
            id = id,
            id_str = id_str,
            in_reply_to_user_id = in_reply_to_user_id, 
            created_at = created_at,
            favourite_count = favourite_count,
            truncated = truncated,
            text = text,
            contributors = contributors, 
            retweet_count = retweet_count,
            in_reply_to_status_id = in_reply_to_status_id,
            filter_level = filter_level,
            quote_count = quote_count,
            geo = geo,
            source = source,
            #place = place,
            possibly_sensitive = possibly_sensitive,
            in_reply_to_screen_name = in_reply_to_screen_name,
            is_quoted_status = is_quoted_status,
            coordinates = coordinates,
            reply_count = reply_count,
            lang =  lang
        )
    else:
        tweet = db_init.Tweet[id]

for t in tweet_json:
    save_data(t)
    commit()
