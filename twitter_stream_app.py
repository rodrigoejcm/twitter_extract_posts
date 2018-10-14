### PARTE 3
##### STREAM FILTRANDO ID DE JORNAIS
##### STREAM ADAPTADA PRO APP 


#github.com/inueni/birdy

from birdy.twitter import StreamClient
import json
import pandas as pd
import pass_tw

def inicializa_cliente_twitter():

    ## Cria DF vazio
    columns = ["id_tweet", "created_at", "text", "user_name" "in_reply_to_id", "retweeted_tweet_d"]
    df = pd.DataFrame(columns=columns)

    client = StreamClient(pass_tw.CONSUMER_KEY,
                        pass_tw.CONSUMER_SECRET,
                        pass_tw.ACCESS_TOKEN,
                        pass_tw.ACCESS_TOKEN_SECRET)

    #response = client.api.users.show.get(screen_name='g1')
     
    return client.stream.statuses.filter.post(follow=['8802752','9317502','14594813'])




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

