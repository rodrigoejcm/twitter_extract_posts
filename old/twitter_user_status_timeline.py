### PARTE 1
##### USER STATUS TIMELINE SEM COMENTARIOS, SO POSTS
#https://github.com/inueni/birdy

from birdy.twitter import UserClient
import json
import pass_tw ## twitter credentials



client = UserClient(pass_tw.CONSUMER_KEY,
                    pass_tw.CONSUMER_SECRET,
                    pass_tw.ACCESS_TOKEN,
                    pass_tw.ACCESS_TOKEN_SECRET)

#response = client.api.users.show.get(screen_name='g1')
response = client.api.statuses.user_timeline.get(screen_name='g1',exclude_replies=False)

with open('/home/rodrigo/Projects/twitter_test_birdy_lib/old/twitter_ust.json', 'a') as my_file:
    json.dump(response.data, my_file)

## PRIMEIRO NIVEL
# text
# id
# created_at
# retweet_count
# lang = 'pt'
# favorite_count
##