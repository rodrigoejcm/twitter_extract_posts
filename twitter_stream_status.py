### PARTE 2
##### STREAM FILTRANDO ID DE JORNAIS.
##### OU O POST DO JORNAL, OU UMA RESPOSTA ou UM RETWIT OU UMA MENCAo...

#https://github.com/inueni/birdy

from birdy.twitter import StreamClient
import atexit
import json
import pandas as pd
import pass_tw ## twitter credentials


## Cria DF vazio
columns = ["id_tweet", "created_at", "text", "user_name" "in_reply_to_id", "retweeted_tweet_d"]
df = pd.DataFrame(columns=columns)


#resultado = []

def exit_handler():
    print('Salvando Tweets')
    with open('/home/rodrigo/Projects/twitter_test_birdy_lib/twitter_ss2.json', 'a') as my_file:
        my_file.write(df.to_json(orient='records', lines=True))
    print('Fim')

atexit.register(exit_handler)


client = StreamClient(pass_tw.CONSUMER_KEY,
                    pass_tw.CONSUMER_SECRET,
                    pass_tw.ACCESS_TOKEN,
                    pass_tw.ACCESS_TOKEN_SECRET)


#response = client.api.users.show.get(screen_name='g1')
resource = client.stream.statuses.filter.post(follow=['8802752','9317502','14594813'])



for data in resource.stream():
    
    if "retweeted_status" in data:
        ret = data.retweeted_status.id
    else:
        ret = False

    df.loc[len(df)] = [data.id,data.created_at,data.text,data.in_reply_to_status_id,ret]
    #resultado.append(data)
    print("Um resultado")

## ID
#14594813 - folha
#9317502 - estadao
#8802752 - G1
##

"id_tweet", "created_at", "text", "user_name" "in_reply_to_id", "retweeted"
## REPONSE JSON
## 1 nivel:
# created_at
# id
# text
# in_reply_to_status_id ( acho que se for RT nao tem nada )
# source ) device )
## 2 nivel:
# user:name
# user:screen_name
# user:id
# user:followers_count (seqguidores)
# user:friends_count ( seguindo )

#retweeted_status:id ( id do tweet original )
#retweeted_status false, quer dizer que nao foi retuitado pelo botao, 
# mas pode ser apenas pelas inclusao do RT


# entities:user_mentions: (id,screen_name,name)
# entities:hashtags (text)
# entities:urls () "expanded_url", "url",  "display_url" )

