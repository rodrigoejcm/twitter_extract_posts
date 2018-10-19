import json
import db_init
import datetime
from pony.orm import *
from dateutil import parser


from birdy.twitter import StreamClient
import pass_tw ## twitter credentials
import unicodedata
from unidecode import unidecode

#import urllib.request
#import urlparse, os





client = StreamClient(pass_tw.CONSUMER_KEY,
                    pass_tw.CONSUMER_SECRET,
                    pass_tw.ACCESS_TOKEN,
                    pass_tw.ACCESS_TOKEN_SECRET)


resource = client.stream.statuses.filter.post(follow=['8802752','9317502','14594813'])


@db_session
def save_data(json_data):

    ### USER ###    

    if 'user' in json_data:

        id_user = json_data['user']['id']
        
        if not db_init.User.exists(id=id_user):
            description = json_data['user']['description'] if 'description' in json_data['user'] else None 
            followers_count = json_data['user']['followers_count'] if 'followers_count' in json_data['user'] else None
            friends_count = json_data['user']['friends_count'] if 'friends_count' in json_data['user'] else None
            id_str_user = json_data['user']['id_str'] if 'id_str' in json_data['user'] else None 
            screen_name = json_data['user']['screen_name'] if 'screen_name' in json_data['user'] else None  
            created_at = parser.parse(json_data['user']['created_at']) if 'created_at' in json_data['user'] else None 
            is_translator = json_data['user']['is_translator'] if 'is_translator' in json_data['user'] else False 
            name = json_data['user']['name'] if 'name' in json_data['user'] else None
            statuses_count = json_data['user']['statuses_count'] if 'statuses_count' in json_data['user'] else None
            verified = json_data['user']['verified'] if 'verified' in json_data['user'] else False
            location = json_data['user']['location'] if json_data['user']['location'] else None
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

        
        ### TWEET ###    

        id = json_data['id']

        if not db_init.Tweet.exists(id=id): 
            id_str = json_data['id_str']
            in_reply_to_user_id = json_data['in_reply_to_user_id'] if 'in_reply_to_user_id' in json_data else None 
            created_at = parser.parse(json_data['created_at'])
            favourite_count = json_data['favourite_count'] if 'favourite_count' in json_data else None 
            truncated = json_data['truncated']
            text = json_data['text']
            if truncated : 
                text_full =  json_data['extended_tweet']['full_text'] 
            else:
                text_full =  None
            contributors = json_data['contributors'] if 'contributors' in json_data else None 
            retweet_count = json_data['retweet_count'] if 'retweet_count' in json_data else None 
            in_reply_to_status_id = json_data['in_reply_to_status_id'] if 'in_reply_to_status_id' in json_data else None 
            filter_level = json_data['filter_level'] if 'filter_level' in json_data else None 
            quote_count = json_data['quote_count'] if 'quote_count' in json_data else None 
            #geo = json_data['geo'] if 'geo' in json_data else None 
            source = json_data['source'] if 'source' in json_data else None 
            possibly_sensitive = json_data['possibly_sensitive'] if 'possibly_sensitive' in json_data else False 
            in_reply_to_screen_name = json_data['in_reply_to_screen_name'] if 'in_reply_to_screen_name' in json_data else None 
            is_quoted_status = json_data['is_quoted_status'] if 'is_quoted_status' in json_data else False 
            #coordinates = json_data['coordinates'] if 'coordinates' in json_data else None 
            reply_count = json_data['reply_count'] if 'reply_count' in json_data else None 
            lang =  json_data['lang'] if 'lang' in json_data else None 
            retweet_from_tweet_id = json_data['retweeted_status']['id'] if 'retweeted_status' in json_data else None 

            tweet = db_init.Tweet(
                user = user,
                id = id,
                id_str = id_str,
                in_reply_to_user_id = in_reply_to_user_id, 
                created_at = created_at,
                favourite_count = favourite_count,
                truncated = truncated,
                text_full = text_full,
                text = text,
                contributors = contributors, 
                retweet_count = retweet_count,
                in_reply_to_status_id = in_reply_to_status_id,
                filter_level = filter_level,
                quote_count = quote_count,
                #geo = geo,
                source = source,
                possibly_sensitive = possibly_sensitive,
                in_reply_to_screen_name = in_reply_to_screen_name,
                is_quoted_status = is_quoted_status,
                #coordinates = coordinates,
                reply_count = reply_count,
                lang =  lang,
                retweet_from_tweet_id = retweet_from_tweet_id
            )
        else:
            tweet = db_init.Tweet[id]

        ### HASHTAGS ###    

        for hashtag in json_data['entities']['hashtags']:
            db_init.Hashtag(tweet = tweet, text = hashtag['text'] )
        
        ### URL ###    

        for url in json_data['entities']['urls']:
            db_init.Url(tweet = tweet, 
                        expanded_url = url['expanded_url'],
                        url = url['url'],
                        display = url['display_url'])
        
        ### USER MENTION ###    

        for mention in json_data['entities']['user_mentions']:
            db_init.UserMention(tweet = tweet, 
                        id_user = mention['id'],
                        name = mention['name'],
                        screen_name = mention['screen_name'])

        ### PLACE ###

        if (json_data['place']):
            full_name = json_data['place']['full_name'] if 'full_name' in json_data['place'] else None 
            place_type = json_data['place']['place_type'] if 'place_type' in json_data['place'] else None 
            country = json_data['place']['country'] if 'country' in json_data['place'] else None 
            country_code = json_data['place']['country_code'] if 'country_code' in json_data['place'] else None  
            name = json_data['place']['name'] if 'name' in json_data['place'] else None 

            db_init.Place( tweet = tweet, 
                            full_name = full_name,
                            name = name,
                            place_type = place_type,
                            country = country,
                            country_code = country_code )
        




                        







    #urllib.request.urlretrieve(
    #    "http://www.digimouth.com/news/media/2011/09/google-logo.jpg", 
    #    "local-filename.jpg")

    #url = 'http://www.plssomeotherurl.com/station.pls?id=111'
    #path = urlparse.urlparse(url).path
    #ext = os.path.splitext(path)[1] ## EXENSION
    


    


for data in resource.stream():
    
    save_data(data)
    commit()

